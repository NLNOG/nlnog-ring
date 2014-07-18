#!/usr/bin/env ruby


module Ring
require 'etc'
Domain  = 'ring.nlnog.net'
User    = Etc.getlogin
Date    = Time.now.utc.strftime '%Y-%m-%d %H:%M:%S (UTC)'
NodeCMD = "dig #{Ring::Domain} txt +short +tcp|tr -d '\"'|tr ' ' '\n'"
Pager   = '/usr/bin/less -R'
SSHCMD  = 'ssh -q -t -C '

class SSH
  require 'net/ssh'
  # takes hostname, command, output string object and optionally usernme as input
  # output is taken as string, instead of returned, so that partial output can be captured
  # returns exit status and timestamp
 
  attr_reader :exit_status, :time
  def self.run node, cmd, output=[], user=Ring::User, &block
    ssh = new node, cmd, output, (Net::SSH::Config.for(node)[:user] or user), &block
    [ssh.exit_status, ssh.time]
  end
  def initialize node, cmd, output, user, &block
    stderr, stdout = '', ''
    @exit_status = 0
    # TODO: Can't use compression, as if connection breaks middle of reading (fail2ban) we may get
    # 'zlib(finalizer): the stream was freed prematurely.' from zlib to stderr. 
    Net::SSH.start(node, user, {:auth_methods=>%w(publickey), :compression=>false}) do |ssh|
      ssh.open_channel do |ch|
        ch.exec(cmd) do |_, ack|
          ch.on_data                   { |_, data| ssh_read data, stdout, :output=>output, :mode=>:stdout, &block}
          ch.on_extended_data          { |_, type, data| ssh_read data, stderr, :output=>output, :mode=>:stderr, &block}
          ch.on_request('exit-status') { |_, data| @exit_status += data.read_long }
          ch.on_request('exit-signal') { |_, data| @exit_status += (data.read_long << 8) }
        end
        ch.wait
      end
      ssh.loop
    end
    @time = Time.now
  end

  private

  # reads ssh output one line at a time, possibly we could allow returning partial lines too
  def ssh_read source, destination, opt={}, &block
    output = opt[:output] || ''
    mode =   opt[:mode]   || :stdout
    destination << source
    lines = destination.lines.to_a
    destination.replace ''
    while line = lines.shift
      if line[-1..-1] == "\n"
        if block_given?
          yield [line, mode]
        else
          output << [line, mode]
        end
      else
        destination.replace line
      end
    end
  end
end

class Open
require 'open3'
  def self.ssh node, cmd, output
    cmd = Ring::SSHCMD + [node, cmd].join(' ')
    popen3 cmd, output
  end
  def self.popen3 cmd, output
    exit_status = 0
    Open3.popen3(cmd) do |stdin, stdout, stderr, waitth|
      while line_err = stderr.gets or line_in = stdout.gets
        output << [line_err, :stderr] if line_err
        output << [line_in, :stdout] if line_in
      end
      #exit_status = waitth.value #this needs ruby1.9
    end
    [exit_status, Time.now]
  end
end

class Lock
  def initialize lock=true
    @lock = lock
  end
  def unlock
    @lock = false
  end
  def lock
    @lock = true
  end
  def locked?
    @lock
  end
end

# returns array of ring node hostnames
def self.nodes
  ## TODO: make it pure ruby, once ring has new enough resolv module with TCP support
  %x(#{Ring::NodeCMD}).split "\n"
end

# replace myself with pager, and run original in child process whose input is directed to mum
def self.pager
  read, write = IO.pipe

  unless fork
    $stdout.reopen(write)
    $stderr.reopen(write) if $stderr.tty?
    read.close
    write.close
    return
  end

  $stdin.reopen(read)
  read.close
  write.close

  exec Ring::Pager
end
end
