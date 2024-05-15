from gpt import gpt
import random
class TestSystem:
    def test_gpt_up(self):
        thing  = gpt()
        history = [{"role":"user", "content":"hey say something funny"}]
        funny_thing, history = thing.run(history)
        print(funny_thing)

TestSystem().test_gpt_up()


