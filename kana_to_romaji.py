import re

def kana_to_romaji(text):

	dict={
		u'きゃ':'kya',u'きゅ':'kyu',u'きょ':'kyo',
		u'しゃ':'sha',u'しゅ':'shu',u'しょ':'sho',
		u'じゃ':'ja',u'じゅ':'ju',u'じょ':'jo',
		u'にゃ':'nya',u'にゅ':'nyu',u'にょ':'nyo',
		
		u'おお':'o',u'おう':'o',
		u'こう':'ko',u'そう':'so',u'とう':'to',u'のう':'no',u'ほう':'ho',u'もう':'mo',u'ろう':'ro',
		u'ごう':'go',u'ぞう':'zo',u'どう':'do',u'ぼう':'bo',
		u'ゆう':'yu',u'よう':'yo',
		u'きょう':'kyo',u'しょう':'sho',u'ちょう':'cho',u'にょう':'nyo',u'ひょう':'hyo',u'みょう':'myo',u'りょう':'ryo',
		
		u'あ':'a',u'い':'i',u'う':'u',u'え':'e',u'お':'o',
		u'か':'ka',u'き':'ki',u'く':'ku',u'け':'ke',u'こ':'ko',
		u'さ':'sa',u'し':'shi',u'す':'su',u'せ':'se',u'そ':'so',
		u'た':'ta',u'ち':'chi',u'つ':'tsu',u'て':'te',u'と':'to',
		u'な':'na',u'に':'ni',u'ぬ':'nu',u'ね':'ne',u'の':'no',
		u'は':'ha',u'ひ':'hi',u'ふ':'fu',u'へ':'he',u'ほ':'ho',
		u'ま':'ma',u'み':'mi',u'む':'mu',u'め':'me',u'も':'mo',
		u'や':'ya',u'ゆ':'yu',u'よ':'yo',
		u'ら':'ra',u'り':'ri',u'る':'ru',u'れ':'re',u'ろ':'ro',
		u'わ':'wa',u'を':'wo',u'ん':'n',
		
		u'が':'ga',u'ぎ':'gi',u'ぐ':'gu',u'げ':'ge',u'ご':'go',
		u'ざ':'za',u'じ':'ji',u'ず':'zu',u'ぜ':'ze',u'ぞ':'zo',
		u'だ':'da',u'ぢ':'di',u'づ':'du',u'で':'de',u'ど':'do',
		u'ば':'ba',u'び':'bi',u'ぶ':'bu',u'べ':'be',u'ぼ':'bo',
		u'ぱ':'pa',u'ぴ':'pi',u'ぷ':'pu',u'ぺ':'pe',u'ぽ':'po',
		
		u'ぁ':'a',u'ぃ':'i',u'ぅ':'u',u'ぇ':'e',u'ぉ':'o',
		u'っ':'tu',
		u'ゃ':'ya',u'ゅ':'yu',u'ょ':'yo',
		u'ゎ':'wa',
		
		u'ゐ':'i',u'ゑ':'e',
		u'ー':'',
		
		u'　':' ',
		
		u'０':'0',u'１':'1',u'２':'2',u'３':'3',u'４':'4',
		u'５':'5',u'６':'6',u'７':'7',u'８':'8',u'９':'9',
		
		u'Ａ':'a',u'Ｂ':'b',u'Ｃ':'c',u'Ｄ':'d',u'Ｅ':'e',u'Ｆ':'f',u'Ｇ':'g',u'Ｈ':'h',u'Ｉ':'i',
		u'Ｊ':'j',u'Ｋ':'k',u'Ｌ':'l',u'Ｍ':'m',u'Ｎ':'n',u'Ｏ':'o',u'Ｐ':'p',u'Ｑ':'q',u'Ｒ':'r',
		u'Ｓ':'s',u'Ｔ':'t',u'Ｕ':'u',u'Ｖ':'v',u'Ｗ':'w',u'Ｘ':'x',u'Ｙ':'y',u'Ｚ':'z',
		
		u'ａ':'a',u'ｂ':'b',u'ｃ':'c',u'ｄ':'d',u'ｅ':'e',u'ｆ':'f',u'ｇ':'g',u'ｈ':'h',u'ｉ':'i',
		u'ｊ':'j',u'ｋ':'k',u'ｌ':'l',u'ｍ':'m',u'ｎ':'n',u'ｏ':'o',u'ｐ':'p',u'ｑ':'q',u'ｒ':'r',
		u'ｓ':'s',u'ｔ':'t',u'ｕ':'u',u'ｖ':'v',u'ｗ':'w',u'ｘ':'x',u'ｙ':'y',u'ｚ':'z',
	}
	
	# Sort key by length descending
	for key in sorted(dict, lambda x,y: cmp(len(y), len(x))):
		value=dict[key]
		p=re.compile(key)
		text=p.sub( value, text )
	
	return text