import pytest
from exp import gen_knowledge_prompting
from exp2 import baseline_prompting
from llama import run_llama as run
from llama2 import run_llama as run2
import random
class TestSystem:
    def test_base_TTT(self):
        content = """a=[1,2,3,4,5,6,7,8,9,10]
-for i in range(1,10):
+for i in range(0,10):
    print(a[i])"""
        assert baseline_prompting(content, "First element in a is not printing", 1)==1
    def test_base_FFF(self):
        content = """import java.util.*"""
        assert baseline_prompting(content, "I'm craving pumpkin pie", 0) == 0
    def test_gen_TTT(self):
        content = """a=[1,2,3,4,5,6,7,8,9,10]
-for i in range(1,10):
+for i in range(0,10):
	print(a[i])"""
        assert gen_knowledge_prompting(content, "First element in a is not printing", 1) == 1
    def test_gen_FTT(self):
        content = """+import random"""
        assert gen_knowledge_prompting(content, "First element in a is not printing", 0) == 0
    def test_gen_TFT(self):
        content = """int *a = {1,2,3,4,5,6,7,8,9,10};
-int i = 1;
-for(i = 1; i<10;i++){
+int i = 0;
+for(i=0l i<10;i++){
	printf(“%d ”,i);
}"""
        assert gen_knowledge_prompting(content, "First element in a is not printing", 1) == 1
    def test_gen_TTF(self):
        content="""a=[1,2,3,4,5,6,7,8,9,10]
-for i in range(1,10):
+for i in range(0,10):
	print(a[i])"""
        assert gen_knowledge_prompting(content, "I am craving pumpkin pie", 1) == 1

    def test_rand_llama(self):
        pool = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789 .,?!"
        for i in range(10):
            prompt = ""
            for j in range(50):
                index = random.randint(0,len(pool)-1)
                choice = pool[index]
                prompt+=choice
            history = {"role":"user", "content":prompt}
            run(history)
    def test_rand_llama2(self):
        pool = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789 .,?!"
        for i in range(10):
            prompt = ""
            for j in range(50):
                index = random.randint(0,len(pool)-1)
                choice = pool[index]
                prompt+=choice
            history = {"role":"user", "content":prompt}
            run2(history)

