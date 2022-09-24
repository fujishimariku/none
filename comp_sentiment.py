import boto3

#感情分析
#テキスト内容と言語コードを取得し分析して結果を返す
def sentimentsearch(text, languagecode):
    comprehend = boto3.client('comprehend')
    return comprehend.detect_sentiment(Text=text, LanguageCode=languagecode)