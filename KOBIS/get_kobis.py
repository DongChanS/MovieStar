import datetime
import requests
import os
from pprint import pprint as pp
import pandas as pd
import time
import urllib.request

class Kobis:
    boxoffice_columns = ['대표코드','name','audiance']
    detail_columns = ["대표코드","open_day","duration","genres","directors","watch_grade","actors"]
    naver_columns = ["대표코드","image","link","avgScore"]
    
    @staticmethod
    def get_request_dict(url,headers=None):
        try:
            return requests.get(url,headers=headers).json()
        except Exception as e:
            print(e)
    
    def __init__(self,last_date,weeks,key):
        self.last_date = last_date
        self.weeks = weeks
        self.dates = []
        self.__key = key
        self.codes = set()
        self.movie_names = set()
        self.quries = set()
        self.actors = set()
        
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
            if movieNm not in self.movie_names:
                self.movie_names.add(movieNm)
                self.codes.add(movieCd)
            else:
                continue
            
            audiAcc = movie.get('audiAcc')
            boxoffice.append([movieCd,movieNm,audiAcc])
        
        return boxoffice 
    
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

    def get_whole_movieinfo(self):
        base_url = "http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieInfo.json"
        movieinfo = []
        
        print("박스오피스 상세정보 수집중...")
        for code in self.codes:
            url = base_url + f"?key={self.__key}&movieCd={code}"
            res_dict = Kobis.get_request_dict(url)['movieInfoResult']['movieInfo']
            
            kor_name = res_dict.get('movieNm')
            self.quries.add(kor_name)
            
            openDt = res_dict.get('openDt')
            showTm = res_dict.get('showTm')
            genres = res_dict.get('genres')
            directors = res_dict.get('directors')
            audits = res_dict.get('audits')
            actors = res_dict.get('actors')

            director_names = "|".join([dir_dict.get('peopleNm') for dir_dict in directors])
            genre_names = "|".join([gen_dict.get('genreNm') for gen_dict in genres])
            if audits:
                watchGradeNms = audits[0].get('watchGradeNm')
            else:
                watchGradeNms = None
            actor_list = [act_dict.get('peopleNm') for act_dict in actors][:3]
            self.actors.update(actor_list)
            actor_names = "|".join([act_dict.get('peopleNm') for act_dict in actors])

            info_list = [code,openDt,showTm,genre_names,director_names,watchGradeNms,actor_names]

            movieinfo.append(info_list)

        self.movie_info = pd.DataFrame(movieinfo,columns=Kobis.detail_columns)
                
    def get_naver_movies(self,NAVER_ID,NAVER_SECRET):
        base_url = "https://openapi.naver.com/v1/search/movie.json"
        naver_movie = []
        headers = {
            "X-Naver-Client-Id" : NAVER_ID,
            "X-Naver-Client-Secret" : NAVER_SECRET
        }
        print("네이버 영화 수집중...")
        
        for query,code in zip(self.quries,self.codes):
            url = base_url + f"?query={query}"
            time.sleep(0.3)
            res_dict = self.get_request_dict(url,headers).get('items')
            if res_dict:
                res_dict = res_dict[0]
            else:
                res_dict = {}
                
            image_url = res_dict.get('image')
            link = res_dict.get('link')
            avg_score = res_dict.get('userRating')
            
            naver_movie.append([code,image_url,link,avg_score])
        
        self.naver_movies = pd.DataFrame(naver_movie,columns=Kobis.naver_columns)
    
    def merge(self):
        merged = pd.merge(kobis.boxoffice, kobis.movie_info, on="대표코드")
        merged = pd.merge(merged, self.naver_movies)
        return merged
    
    def all_in_one(self,NAVER_ID,NAVER_SECRET):
        self.get_dates()
        self.get_whole_boxoffice()
        self.get_whole_movieinfo()
        self.get_naver_movies(NAVER_ID,NAVER_SECRET)
        return self.merge()
    
    def get_actor_info(self, actor_name):
        base_url = "http://www.kobis.or.kr/kobisopenapi/webservice/rest/people/searchPeopleList.json"
        url = base_url + f"?key={self.__key}&peopleNm={actor_name}&itemPerPage=1"
        
        return Kobis.get_request_dict(url)['peopleListResult']['peopleList']
    
    def get_actor_image(self,actor_name,NAVER_ID,NAVER_SECRET):
        base_url = "https://openapi.naver.com/v1/search/image"
        url = base_url + f"?query={actor_name}&sort=sim&filter=large&display=1"

        headers = {
            "X-Naver-Client-Id" : NAVER_ID,
            "X-Naver-Client-Secret" : NAVER_SECRET
        }

        return Kobis.get_request_dict(url, headers)['items']
    
    
    def get_whole_actor_data(self,NAVER_ID,NAVER_SECRET):
        
        actor_infos = []
        
        for name in self.actors:
            kobis_res = self.get_actor_info(name)
            if kobis_res:
                filmo_names = kobis_res[0]['filmoNames']
            else:
                continue
                
            naver_res = self.get_actor_image(name,NAVER_ID,NAVER_SECRET)
            if naver_res:
                profile_img = naver_res[0]['link']
            else:
                continue
                
            actor_infos.append([name, filmo_names, profile_img])
        
        self.actor_infos = pd.DataFrame(actor_infos, columns=['이름','출연작','이미지링크'])