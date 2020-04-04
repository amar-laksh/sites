src = $(wildcard $(CURDIR)/*.s)
bin = $(basename $(src))
obj = $(addsuffix .o, $(bin))

$(bin): $(obj)
	ld -o $@ -m  elf_i386  $<

$(obj): $(src)
	nasm -o $@ -f elf $<

.PHONY: clean

clean:
	rm -f $(obj) $(bin)
