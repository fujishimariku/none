import boto3

#翻訳
#テキスト内容と翻訳先言語コードを取得し結果を返す
def translate(text, TargetLanguageCode):
    translate = boto3.client('translate')
    return translate.translate_text(Text=text, SourceLanguageCode="auto", TargetLanguageCode=TargetLanguageCode)