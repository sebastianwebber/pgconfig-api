require 'json'
require_relative '../lib/bash_command'

RSpec.describe BashCommand, "#build" do
    context "Build the bash lines to compose a script" do 

        before(:context) do
            @json_instruction = JSON.parse('{ "command": { "lines": [ "cat /etc/fstab", "echo ${VARIABLE_XPTO} > /tmp/teste.txt" ], "options": { "syntax": "bash", "show-lines": "true" }}}')
        end

        it "should contains a hash bang at first line" do
            expect(BashCommand.new(@json_instruction).build.first).to eq("#!/bin/bash")
        end

        it "should contains the fstab cat command" do
            expect(BashCommand.new(@json_instruction).build[1]).to eq("cat /etc/fstab")
        end

        it "should build bash commands based on instruction" do
            expect(BashCommand.new(@json_instruction).build.last).to eq("echo ${VARIABLE_XPTO} > /tmp/teste.txt")
        end

    end
end