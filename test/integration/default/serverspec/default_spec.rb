require 'spec_helper'

describe user('pdns'), :if => ['debian', 'ubuntu'].include?(os[:family]) do
  it { should exist }
  it { should belong_to_group('pdns') }
end

describe user('pdns-recursor'), :if => os[:family] == 'redhat' do
  it { should exist }
  it { should belong_to_group('pdns-recursor') }
end

describe service('pdns-recursor') do
  it { should be_enabled }
  if !(os[:family] == 'ubuntu' and os[:release] == '14.04')
    # Ubuntu 14.04's pdns-recursor service does not support the status command
    it { should be_running }
  end
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
  if ['debian', 'ubuntu'].include?(os[:family])
    its(:user) { should eq "pdns" }
    its(:group) { should eq "pdns" }
  elsif os[:family] == 'redhat'
    its(:user) { should eq "pdns-recursor" }
    its(:group) { should eq "pdns-recursor" }
  end
end
