class BashCommand 

    def initialize instruction = nil
        @instruction = instruction
    end

    def build
        resultado = [ "#!/bin/bash"] 
        # puts @instruction.inspect
        resultado += @instruction["session"].first["instructions"].first["command"]["lines"] if @instruction != nil
        resultado
    end
end
