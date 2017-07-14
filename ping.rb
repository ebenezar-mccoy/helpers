#!ruby
require 'net/ping'

module Enumerable
  def sum
    self.inject(0) { |accum, i| accum + i }
  end
  def mean
    self.sum/self.length.to_f
  end
  def sample_variance
    m = self.mean
    sum = self.inject(0){|accum, i| accum +(i-m)**2 }
    sum/(self.length - 1).to_f
  end
  def standard_deviation
    return Math.sqrt(self.sample_variance)
  end
end

host = ARGV[0]
icmp = Net::Ping::ICMP.new(host)
ping_array = []
math_array = []
pingfails = 0
pings_transimted = 0
started = Time.now

begin
  (1..10000).each do
    if icmp.ping
      ping_ms = (icmp.duration * 1000).round(3)
      math_array << ping_ms
      ping_array << [Time.now.strftime("%m/%e/%y %H:%M:%S"), ping_ms]
      print "#{Time.now.strftime('%H:%M:%S')}  #{ping_ms} ms".ljust(22, " ")
      ping_int = ping_ms.to_i/10
      puts "".ljust(ping_int, ".")
      pings_transimted += 1
      sleep(1)
    else
      pingfails += 1
      puts "timeout"
    end
  end
rescue SystemExit, Interrupt
ensure
  ended = Time.now
  received = pings_transimted - pingfails
  loss = ((pingfails / pings_transimted)*100).round(1)

  avg = math_array.mean.round(3)
  min = math_array.min.round(3)
  max = math_array.max.round(3)
  stdev = math_array.standard_deviation.round(3)
  puts "\n\nStarted: #{started}"
  puts "Ended: #{ended}"
  puts "Took: #{ended - started}\n\n"

  puts "#{pings_transimted} packets transmitted, #{received} received, #{loss}% packet loss"
  puts "round-trip min/avg/max/stddev = #{min}/#{avg}/#{max}/#{stdev} ms"

  times = []
  (0..9).each { |t| times[t] = 0 }

  ping_array.each do |time, ping|
    times[0] += 1 if ping < 100
    (1..9).each do |t|
      time = t.to_s + '00'
      time_end = (t + 1).to_s + '00'
      if t == 9
        times[t] += 1 if ping > time.to_i
      else
        times[t] += 1 if ping > time.to_i && ping < time_end.to_i
      end
    end
  end
  puts "\nStatistics: "
  puts "[ <100 | >100 | >200 | >300 | >400 | >500 | >600 | >700 | >800 | >900 ]"
  printf("[  %-3s |  %-3s |  %-3s |  %-3s |  %-3s |  %-3s |  %-3s |  %-3s |  %-3s |  %-3s ]\n\n", times[0], times[1],
    times[2], times[3], times[4], times[5], times[6], times[7], times[8], times[9])
end
