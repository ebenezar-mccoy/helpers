require 'typhoeus'

abort "Usage: #{$PROGRAM_NAME} [request] [concurrent] [how_many_requests]" unless ARGV.length == 3

data = []
start = Time.now

hydra = Typhoeus::Hydra.new(max_concurrency: ARGV[1].to_i)

ARGV[2].to_i.times do
  request = Typhoeus::Request.new(ARGV[0])
  if ARGV[0] =~ %r{ecr/rad2/brs/file}
    request = Typhoeus::Request.new(
      ARGV[0],
      method: :post,
      body: '6146G32#?W',
      headers: { 'Content-Type' => 'application/octet-stream' }
    )
  end
  request.on_complete do |response|
    if response.success?
      puts "#{Time.now}: code: #{response.code} respone.time: #{response.time}"
      data << [response.time, response.app_connect_time]
    elsif response.timed_out?
      puts('got a time out')
    elsif response.code == 0
      puts(response.return_message)
    else
      puts('HTTP request failed: ' + response.code.to_s)
    end
  end
  hydra.queue(request)
end
hydra.run

avg_time             = 0
avg_app_connect_time = 0

data.each do |time, app_connect_time|
  avg_time             += time
  avg_app_connect_time += app_connect_time
end

finish = Time.now
took = finish - start

puts "took #{took}"
puts "avg response.time for #{data.size} requests #{avg_time / Float(data.size)}"
