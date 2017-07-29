class BashTemplate 

    def initialize instruction = nil
        @instruction = instruction
    end

    def build
        resultado = [ "#!/bin/bash"] 

        @instruction["session"].each do |detail|
            resultado += detail["instructions"].first["command"]["lines"]
        end if @instruction != nil

        resultado
    end
end
