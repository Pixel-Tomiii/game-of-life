from gameoflife import gameoflife

if __name__ == "__main__":
    gameoflife.load_config(".config")
    gameoflife.generate("test.grid")
    gameoflife.loop()
