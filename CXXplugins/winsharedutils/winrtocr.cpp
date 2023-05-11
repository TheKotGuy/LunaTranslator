#include"pch.h"
#include"define.h"
#include<windows.h>
#include <winrt/Windows.Foundation.h>
#include <winrt/Windows.Storage.Pickers.h>
#include <winrt/Windows.Storage.Streams.h>
#include <winrt/Windows.Graphics.Imaging.h>
#include <winrt/Windows.Media.FaceAnalysis.h>
#include <winrt/Windows.Media.Ocr.h>

#include <winrt/Windows.Foundation.Collections.h>
#include <winrt/Windows.Devices.Enumeration.h>
#include <winrt/Windows.Media.Devices.h>

#include <winrt/Windows.Security.Cryptography.h>
#include <winrt/Windows.Globalization.h>
#include <iostream>
#include <fstream>
#include<vector>
using namespace winrt;

using namespace Windows::Foundation;
using namespace Windows::Storage;
using namespace Windows::Storage::Streams;
using namespace Windows::Graphics::Imaging;
using namespace Windows::Media::Ocr;

using namespace Windows::Devices::Enumeration;
using namespace Windows::Media::Devices;

using namespace Windows::Security::Cryptography;
using namespace Windows::Globalization;
using namespace Windows::Foundation::Collections;
bool check_language_valid(wchar_t* language) {
    OcrEngine ocrEngine = OcrEngine::TryCreateFromUserProfileLanguages();
    std::wstring l = language;
    try {
        Language language1(l);
        return ocrEngine.IsLanguageSupported(language1);
    }
    catch (...) {
        return false;
    }
}
wchar_t** getlanguagelist(int* num) {
    OcrEngine ocrEngine = OcrEngine::TryCreateFromUserProfileLanguages();
    auto languages = ocrEngine.AvailableRecognizerLanguages();
    auto ret = new wchar_t* [languages.Size()];
    int i = 0;
    for (auto&& language : languages)
    {
        //std::wcout << language.LanguageTag().c_str() << L" " << language.DisplayName().c_str() << L" " << language.AbbreviatedName().c_str() << L'\n';
        //zh-Hans-CN  ����(���壬�й�)  ����
        //ja  ����   
        auto lang = language.LanguageTag();
        size_t len = lang.size() + 1;
        ret[i] = new wchar_t[len];
        wcscpy_s(ret[i], len, lang.c_str());
        i += 1;
    }
    *num = languages.Size();
    return ret;
}
ocrres OCR(wchar_t* fname, wchar_t* lang, wchar_t* space, int* num)
{
    // ָ��Ҫʶ���ͼ���ļ�·��
    std::wstring imagePath = fname;

    // ��ͼ���ļ�
    StorageFile imageFile = StorageFile::GetFileFromPathAsync(imagePath).get();
    IRandomAccessStream imageStream = imageFile.OpenAsync(FileAccessMode::Read).get();
    // ���� BitmapDecoder �������ͼ��
    BitmapDecoder decoder = BitmapDecoder::CreateAsync(imageStream).get();

    // �ӽ������л�ȡλͼ����
    SoftwareBitmap softwareBitmap = decoder.GetSoftwareBitmapAsync().get();
    std::wstring l = lang;
    Language language(l);
    // ���� OcrEngine ����
    OcrEngine ocrEngine = OcrEngine::TryCreateFromLanguage(language);
    // ���� OcrResult ���󲢽���ʶ��
    OcrResult ocrResult = ocrEngine.RecognizeAsync(softwareBitmap).get();
    // ���ʶ����
    auto res = ocrResult.Lines(); 
    std::vector<std::wstring>rets;
    std::vector< int>ys; 
    int i = 0;
    std::wstring sspace = space;//Ĭ�ϼ�ʹ����Ҳ�пո�
    for (auto line : res)
    {

        std::wstring xx = L"";
        bool start = true;
        float y = 0;
        for (auto word : line.Words()) {
            if (!start)xx += sspace;
            start = false;
            xx += word.Text();
            y = word.BoundingRect().Y;
        }
        ys.push_back(y);
        rets.emplace_back(xx); 
        i += 1;
    }
    *num = res.Size();
    return ocrres{ vecwstr2c(rets),vecint2c(ys)};
}
