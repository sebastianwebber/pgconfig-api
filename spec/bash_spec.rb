require 'json'
require_relative '../lib/bash_template'

RSpec.describe BashTemplate, "#build" do
    context "Build the bash lines to compose a script" do 

        before(:context) do
            @json_instruction = JSON.parse('{"ui-options":{"auto-enumerate":"true","field-list":[{"key":"$VARIABLE_XPTO","options":{"name":"xpto","description":"do xpto stuff","type":"number","default-value":"foo"}}]},"session":[{"name":"Run XPTO stuff","text-top":["Brief explanation goes here."],"instructions":[{"text-top":["`xpto` is pretty important. ","Now, run the command `xpto` and makes stuff:"],"command":{"lines":["cat /etc/fstab","echo ${VARIABLE_XPTO} > /tmp/teste.txt"],"options":{"syntax":"bash","show-lines":"true"}},"text-bottom":["Bottom text about this command."]}],"text-bottom":["Conclusion goes here."]},{"name":"Run zero_command stuff","text-top":["Brief explanation goes here."],"instructions":[{"text-top":["`zero_command` is pretty important. ","Now, run the command `zero_command` and makes stuff:"],"command":{"lines":["zero_command >> /tmp/teste.txt"],"options":{"syntax":"bash","show-lines":"true"}},"text-bottom":["Bottom text about this command."]}],"text-bottom":["Conclusion goes here."]}]}')
        end

        it "should contains a hash bang at first line" do
            expect(BashTemplate.new(@json_instruction).build.first).to eq("#!/bin/bash")
        end

        it "should contains the fstab cat command" do
            expect(BashTemplate.new(@json_instruction).build[1]).to eq("cat /etc/fstab")
        end

        it "should build bash commands based on instruction from json" do
            expect(BashTemplate.new(@json_instruction).build.last).to eq("zero_command >> /tmp/teste.txt")
        end

        it "should support multiple sessions in the json document" do
            array_data = ["#!/bin/bash", "cat /etc/fstab", "echo ${VARIABLE_XPTO} > /tmp/teste.txt", "zero_command >> /tmp/teste.txt"]
            expect(BashTemplate.new(@json_instruction).build).to eq(array_data)
        end
    end
end