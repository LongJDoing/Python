# Question_Demo
## 1. Rapidjson File:
**在ios崩溃的原因:**这个是你的转换代码里面的问题，和2dx引擎无关。下面这个函数
```
    CCString* KSCCJsonRapid::jsonStringFromDictionary(CCDictionary *dic)
    {
        rapidjson::Value *value = KSCCJsonRapid::jsonValueFromDictionary(dic);
        rapidjson::StringBuffer buffer;
        rapidjson::Writerrapidjson::StringBuffer writer(buffer);
        value->Accept(writer);
        std::string jsonString = buffer.GetString();
        delete value;
        return CCString::create(jsonString);
    }
```
*第一行获取rapidjson::Value并没有传入第二个参数document，你可以看看jsonValueFromDictionary函数里面的实现。*<br>
*它创建了一个document用来生成Value，然后在函数退出之前删除了这个document，在pc上内存充足，*<br>
*释放后并不会马上被重新分配使用，但是设备上的内存比较少，释放后马上被回收，导致返回的value已经无效，*<br>
*再访问的时候就会产生非法访问。只要在上面这个函数调用KSCCJsonRapid::jsonValueFromDictionary之前自己创建一个document对象，*<br>
*传入函数。生成字符串后再释放就可以解决崩溃问题。*<br>

## 2. Shatter Effect File
