general_compile_options = -Werror -Wextra -Wall 
style_compile_options = -Wparentheses -pedantic -Wunused-variable
variable_compile_options = -Wfloat-equal -Wconversion -Wunused-parameter -Wredundant-decls -Wunused-value -Wuninitialized  
func_compile_options = -Wreturn-type -Wunused-function -Wswitch-default  -Winit-self



CC 		:= gcc
CFLAGS 	:= -O3 -g $(general_compile_options) #$(style_compile_options) $(variable_compile_options) $(func_compile_options)

DEPS = bangbang.c

all: $(DEPS)
	$(CC) $(DEPS) -o bangbang.so -fPIC -shared

clean:
	rm -rf *so
