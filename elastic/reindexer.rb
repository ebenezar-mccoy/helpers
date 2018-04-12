require 'net/http'
require 'json'

def read_indexes
  @lista = File.read(ARGV[0]).split("\n")
rescue Errno::ENOENT => ex
  raise(ex)
end

def reindex(from, to)
  uri = URI('http://some.server:9200/_reindex')
  req = Net::HTTP::Post.new(uri, 'Content-Type' => 'application/json')
  req.body = { source: { index: from }, dest: { index: to } }.to_json
  puts "#{Time.now} -> reindex[#{from} -> #{to}]: request sent"
  res = Net::HTTP.start(uri.hostname, uri.port, read_timeout: 5000) do |http|
    http.request(req)
  end
  puts "#{Time.now} -> reindex[#{from} -> #{to}]: #{res.code}"
rescue Errno::ENOENT => ex
  raise(ex)
end

def delete_index(index)
  uri = URI("http://some.server:9200/#{index}")
  req = Net::HTTP::Delete.new(uri)
  res = Net::HTTP.start(uri.hostname, uri.port, read_timeout: 5000) do |http|
    http.request(req)
  end
  puts "#{Time.now} -> delete_index[#{index}]: #{res.code}"
rescue Errno::ENOENT => ex
  raise(ex)
end

#
# Main

read_indexes

@lista.each do |index|
  reindex(index, "#{index}-new")
  delete_index(index)
  reindex("#{index}-new", index)
  delete_index("#{index}-new")
end
