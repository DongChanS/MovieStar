import datetime
import requests
import os
from pprint import pprint as pp
import pandas as pd
import time
import urllib.request

class Kobis:
    boxoffice_columns = ['대표코드','영화명','누적관객수','해당일']
    detail_columns = ["대표코드","영화명(국문)","영화명(영문)","영화명(원문)",
              "개봉연도","상영시간","장르","감독","관람등급","배우1","배우2","배우3"]
    naver_columns = ["대표코드","img_url","link","평점"]
    
    @staticmethod
    def get_request_dict(url,headers=None):
        try:
            return requests.get(url,headers=headers).json()
        except Exception as e:
            print(e.message, e.args)
    
    def __init__(self,last_date,weeks,key):
        self.last_date = last_date
        self.weeks = weeks
        self.dates = []
        self.__key = key
        self.codes = []
        
    def get_dates(self):
        dates = [self.last_date-x*datetime.timedelta(7) for x in range(self.weeks)]
        self.dates = [date.strftime('%Y%m%d') for date in dates]
    
    def get_one_boxoffice(self,date):
        base_url = "http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchWeeklyBoxOfficeList.json"
        url = base_url + f"?key={self.__key}&targetDt={date}&weekGb=0"
        res_dict = Kobis.get_request_dict(url)
        weekly_dict = res_dict['boxOfficeResult']['weeklyBoxOfficeList']
        boxoffice = []
        
        for movie in weekly_dict:
            movieCd = movie.get('movieCd')
            movieNm = movie.get('movieNm')
            audiAcc = movie.get('audiAcc')
            boxoffice.append([movieCd,movieNm,audiAcc,date])
            
        return boxoffice
    
    @staticmethod
    def modify_audiAcc(df):
        each_movies = []
        
        for key in df.groupby('영화명').groups:
            movie_indices = df.groupby('영화명').groups[key]
            movie_df = df.loc[movie_indices]
            movie_df['누적관객수'] = movie_df['누적관객수'].describe()['top']
            each_movies.append(movie_df)

        result = pd.concat(each_movies)
        result = result.reset_index()
        result = result.drop(['index'],axis=1)

        return result 
    
    
    def get_whole_boxoffice(self):
        boxoffice_list = []
        for date in self.dates:
            while(True):
                try:
                    boxoffice_list.extend(self.get_one_boxoffice(date))
                    print(date+" 일자 boxoffice 정보 수집 완료!")
                    break
                except Exception as e:
                    print(e.message, e.args)
        
        self.boxoffice = pd.DataFrame(boxoffice_list,columns=Kobis.boxoffice_columns)
        self.boxoffice = self.boxoffice.reset_index()
        self.boxoffice = self.boxoffice.drop('index',axis=1)
        
        return Kobis.modify_audiAcc(self.boxoffice)
    
    @staticmethod
    def save_to_csv(df,filename):
        df.to_csv(filename)
    
    def get_movieCds(self):
        self.codes = pd.unique(self.boxoffice['대표코드'])

    def get_whole_movieinfo(self):
        base_url = "http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieInfo.json"
        movieinfo = []
    
        for code in self.codes:
            url = base_url + f"?key={self.__key}&movieCd={code}"
            res_dict = Kobis.get_request_dict(url)['movieInfoResult']['movieInfo']

            movieNm = res_dict.get('movieNm')
            movieNmEn = res_dict.get('movieNmEn')
            movieNmOg = res_dict.get('movieNmOg')
            openDt = res_dict.get('openDt')
            showTm = res_dict.get('showTm')
            genres = res_dict.get('genres')
            directors = res_dict.get('directors')
            audits = res_dict.get('audits')
            actors = res_dict.get('actors')

            director_names = "/".join([dir_dict.get('peopleNm') for dir_dict in directors])
            genre_names = "/".join([gen_dict.get('genreNm') for gen_dict in genres])
            watchGradeNms = audits[0].get('watchGradeNm')
            actor_names = [act_dict.get('peopleNm') for act_dict in actors[:3]]
            actor_names += ["" for _ in range(len(actor_names),3)]

            info_list = [code,movieNm,movieNmEn,movieNmOg,openDt,showTm,
                             genre_names,director_names,watchGradeNms]+actor_names

            movieinfo.append(info_list)
            print(movieNm+" 영화 정보 수집 완료!")
            
        self.movie_info = pd.DataFrame(movieinfo,columns=Kobis.detail_columns)
        
        return self.movie_info
        
    def get_naver_movies(self,naver_id,naver_key):
        base_url = "https://openapi.naver.com/v1/search/movie.json"
        naver_movie = []
        
        for query,code in zip(self.quries,self.codes):
            url = base_url + f"?query={query}"
            headers = {
                "X-Naver-Client-Id" : naver_id,
                "X-Naver-Client-Secret" : naver_key
            }
            res_dict = self.get_request_dict(url,headers).get('items')[0]
            image_url = res_dict.get('image')
            link = res_dict.get('link')
            avg_score = res_dict.get('userRating')
            time.sleep(0.5)
            naver_movie.append([code,image_url,link,avg_score])
            print(query+" 네이버 영화 정보 수집 완료!")
        
        return pd.DataFrame(naver_movie,columns=Kobis.naver_columns)
    
    
    def get_quries(self):
        self.quries = self.movie_info['영화명(국문)']
    
    @staticmethod
    def image_download(url,filename):
        urllib.request.urlretrieve(url,filename)
        

if __name__ == "__main__":
    KOBIS_KEY = os.environ['KOBIS_KEY']
    kobis = Kobis(datetime.date(2019,4,1),5,KOBIS_KEY)
    #------------------
    kobis.get_dates()
    boxoffice_df = kobis.get_whole_boxoffice()
    # kobis.save_to_csv(boxoffice_df,"boxoffice.csv")
    #------------------
    kobis.get_movieCds()
    movieinfo_df = kobis.get_whole_movieinfo()
    # kobis.save_to_csv(movieinfo_df,"movie.csv")
    #-------------------
    kobis.get_quries()
    NAVER_ID = os.environ['NAVER_ID']
    NAVER_SECRET = os.environ['NAVER_SECRET']
    naver_df = kobis.get_naver_movies(NAVER_ID,NAVER_SECRET)
    # kobis.save_to_csv(naver_df,"movie_naver.csv")
    #-----------------
   