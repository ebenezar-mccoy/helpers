#!/opt/chefdk/embedded/bin/ruby

require 'net/http'
require 'json'
require 'mixlib/shellout'

abort("#{$PROGRAM_NAME} environment group [time period in minutes] reason") unless ARGV.length == 4

env = ARGV[0]
group = ARGV[1]
period = ARGV[2]
reason = ARGV[3]

def knife(cmd)
  knife = Mixlib::ShellOut.new(cmd)
  knife.run_command
  knife.stdout.tr("\n", '').gsub('.some.domain', '')
end

def hc_name(group, env)
  cmd = "knife search 'chef_environment:#{env} AND hc_name:#{group}' -i -c /opt/teamcity-chef/knife.rb"
  hc = knife(cmd)
  abort("[#{group}]: Unable to find server group. (app_server)") if hc.empty?
  hc
end

def zabbix_id(group, env)
  uri = URI('http://some.server/zabbix/api_jsonrpc.php')
  req = Net::HTTP::Post.new(uri, 'Content-Type' => 'application/json')
  req.body = {
    jsonrpc: '2.0',
    method: 'host.get',
    params: {
      output: 'extend',
      filter: { host: "#{hc_name(group, env)}_#{group}" }
    },
    auth: 'some_token',
    id: '1'
  }.to_json
  res = Net::HTTP.start(uri.hostname, uri.port) do |http|
    http.request(req)
  end
  ress = instance_eval(res.body)
  abort("[#{group}]: Unable to find server group. (zabbix)") if ress[:result].empty?
  ress[:result][0][:hostid]
end

def set_maintanence(period, reason, group, env)
  uri = URI('http://some.server/zabbix/api_jsonrpc.php')
  req = Net::HTTP::Post.new(uri, 'Content-Type' => 'application/json')
  per = period.to_i * 60
  from = Time.now.to_i
  to = (Time.now + per).to_i
  id = zabbix_id(group, env)
  req.body = {
    jsonrpc: '2.0',
    method: 'maintenance.create',
    params: {
      name: "#{env} #{group} #{reason}",
      active_since: from, active_till: to,
      hostids: [id],
      timeperiods: [{ period: per }]
    },
    auth: 'some_token',
    id: '1'
  }.to_json
  res = Net::HTTP.start(uri.hostname, uri.port) do |http|
    http.request(req)
  end
  begin
    ress = instance_eval(res.body)
  rescue
    ress = {}
    ress['result'] = res.body
  end
  puts ress[:result]
end

set_maintanence(period, reason, group, env)
