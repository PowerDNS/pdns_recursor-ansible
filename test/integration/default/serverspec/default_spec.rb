require 'spec_helper'

describe user('pdns') do
  it { should exist }
  it { should belong_to_group('pdns') }
end

describe service('pdns-recursor') do
  it { should be_enabled }
  it { should be_running }
end

describe port(53) do
  it { should be_listening.with('udp') }
  it { should be_listening.with('tcp') }
end

describe file('/etc/powerdns/recursor.conf') do
  it { should be_file }
  it { should be_owned_by 'root' }
  it { should be_grouped_into 'root' }
end

describe process('pdns_recursor') do
  its(:user) { should eq "pdns" }
  its(:group) { should eq "pdns" }
end
