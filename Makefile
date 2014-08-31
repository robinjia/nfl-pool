CC=gcc
CFLAGS=-c -Wall -O2
VPATH=src/c
BUILD_DIR=build

all: checkdirs $(BUILD_DIR)/test/bitset_test Makefile

check: all
	$(BUILD_DIR)/test/bitset_test

checkdirs: $(BUILD_DIR)/test

$(BUILD_DIR)/test:
	mkdir -p $(BUILD_DIR)/test

$(BUILD_DIR)/test/bitset_test: $(BUILD_DIR)/bitset.o $(BUILD_DIR)/test/bitset_test.o
	$(CC) $(BUILD_DIR)/bitset.o $(BUILD_DIR)/test/bitset_test.o -o $(BUILD_DIR)/test/bitset_test

$(BUILD_DIR)/%.o: %.c
	$(CC) $(CFLAGS) $< -o $@

clean:
	rm -rf $(BUILD_DIR)
