require 'spec_helper'

if os[:family] == 'debian' and os[:release] =~ /8\./
  describe file('/etc/powerdns/recursor.conf') do
    its(:content) { should contain "allow-from=127.0.0.1/24" }
    its(:content) { should match /allow-from\+=::1\/127/ }
  end
end

if os[:family] == 'redhat'
  describe file('/etc/pdns-recursor/recursor.conf') do
    its(:content) { should contain "allow-from=127.0.0.1/24, ::1/127" }
  end
end

if os[:family] == 'ubuntu' and os[:release] == '14.04'
  describe file('/etc/powerdns/recursor.conf') do
    its(:content) { should contain "allow-from=127.0.0.1/24, ::1/127" }
  end
end
