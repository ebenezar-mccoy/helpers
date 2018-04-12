require 'net/http'
require 'json'
require 'base64'
require 'pp'

apki = instance_eval(File.read('zbior_apek'))
# apki = [{ id: "MP_APP_MplatformRad2_RsmWar_IntegrationPackage", name: 'integration :: package' }]

def teamcity_get_parameters(url, what)
  uri = URI("http://chepri.comp-ci.net:8111/app/rest/buildTypes/id:#{url}#{what}")
  req = Net::HTTP::Get.new(uri, 'Content-Type' => 'text/plain')
  # req.basic_auth 'user', Base64.decode64("")
  res = Net::HTTP.start(uri.hostname, uri.port) do |http|
    http.request(req)
  end
  response = res.body
  response = '' if res.body =~ /404/
  response
end

def teamcity_send_parameters(url, what, put)
  uri = URI("http://chepri.comp-ci.net:8111/app/rest/buildTypes/id:#{url}#{what}")
  req = Net::HTTP::Put.new(uri, 'Content-Type' => 'text/plain')
  # req.basic_auth 'user', Base64.decode64("")
  req.body = put
  res = Net::HTTP.start(uri.hostname, uri.port) do |http|
    http.request(req)
  end
  response = res.body
  response = '' if res.body =~ /404/
  response
end

apki.each do |apka|
  next unless apka[:id] =~ /Prod/
  printf "before: APP  %-25s NAME  %-22s  JVM  %-18s  VER %s \n",
    apka[:name],
    teamcity_get_parameters(apka[:id], '/name'),
    teamcity_get_parameters(apka[:id], '/parameters/wildfly_profile'),
    teamcity_get_parameters(apka[:id], '/parameters/Major.Minor')

  printf " after: APP  %-25s NAME  %-22s  JVM  %-18s  VER %s \n",
    apka[:name],
    teamcity_send_parameters(apka[:id], '/name', apka[:name]),
    teamcity_send_parameters(apka[:id], '/parameters/wildfly_profile', apka[:wildfly_profile]),
    teamcity_send_parameters(apka[:id], '/parameters/Major.Minor', apka[:version])
end
