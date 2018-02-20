import re


class StopWordRemover:
    def stopwordRemoval(self, string):
        # stop words list
        filehandler = open("preprocessing/stopwordlist.txt").read().decode("ascii", "ignore")
        stopwords = filehandler.split()
        # print(stopwords)
        # stopwords = ["yang", "dengan", "itu", "ya", "di", "maksud", "ini", "dimaksud", "untuk","siapa",
        # 				"siapakah","dimana","dimanakah","kemana","kemanakah",
        # 				"darimana","darimanakah","kapan","kapankah","berapa","berapakah",
        # 				"apa","apakah","mengapa","kenapa","bagaimana","bagaimanakah","dapat","karena","itu",
        # 				"sebaliknya","penyakit","atau","sedang"]

        checks = string.split()
        output = ""

        for c in checks:
            c = re.sub('[^A-Za-z]+', ' ', c)
            # c = c.translate(None, digits)
            if c not in stopwords:
                output = output + " " + c

        return str(output[1:])
