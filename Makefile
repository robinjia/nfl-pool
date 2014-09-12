CC=gcc
CFLAGS=-c -std=c99 -Wall -Wstrict-prototypes -O2
VPATH=src/c
BUILD_DIR=build
BINARIES=$(BUILD_DIR)/choose-picks $(BUILD_DIR)/compare-picks $(BUILD_DIR)/test/bitset-test $(BUILD_DIR)/test/picks-test

all: checkdirs $(BINARIES) Makefile

check: all
	$(BUILD_DIR)/test/bitset-test
	$(BUILD_DIR)/test/picks-test

debug: CC += -DDEBUG -g -O0
debug: all

checkdirs: $(BUILD_DIR)/test

$(BUILD_DIR)/test:
	mkdir -p $(BUILD_DIR)/test

$(BUILD_DIR)/choose-picks: $(BUILD_DIR)/choose_picks.o $(BUILD_DIR)/picks.o $(BUILD_DIR)/predictions.o
	$(CC) $(BUILD_DIR)/choose_picks.o $(BUILD_DIR)/picks.o $(BUILD_DIR)/predictions.o -o $(BUILD_DIR)/choose-picks

$(BUILD_DIR)/compare-picks: $(BUILD_DIR)/compare_picks.o $(BUILD_DIR)/picks.o $(BUILD_DIR)/predictions.o
	$(CC) $(BUILD_DIR)/compare_picks.o $(BUILD_DIR)/picks.o $(BUILD_DIR)/predictions.o -o $(BUILD_DIR)/compare-picks

$(BUILD_DIR)/test/picks-test: $(BUILD_DIR)/test/picks_test.o
	$(CC) $(BUILD_DIR)/picks.o $(BUILD_DIR)/predictions.o $(BUILD_DIR)/test/picks_test.o -o $(BUILD_DIR)/test/picks-test

$(BUILD_DIR)/test/bitset-test: $(BUILD_DIR)/test/bitset_test.o
	$(CC) $(BUILD_DIR)/test/bitset_test.o -o $(BUILD_DIR)/test/bitset-test

$(BUILD_DIR)/%.o: %.c
	$(CC) $(CFLAGS) $< -o $@

.PHONY : clean

clean:
	rm -rf $(BINARIES) $(BUILD_DIR)/*.o $(BUILD_DIR)/test/*.o
