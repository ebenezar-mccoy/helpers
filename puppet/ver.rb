#!/bin/ruby
require 'yaml'

YAML.load_file(ARGV[1])["ccdev::deployments::versions"][ARGV[0]].each do |app|
  app[1].each do |x,y|
    v = y.split(':')
    printf("%-35s %-15s %s \n", v[1], v[2], v[3]) if x == 'gav'
  end
end

