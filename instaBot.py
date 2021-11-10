import instaloader
import re
from time import sleep


class InstaBot:
    def user_information(self, username):
        L = instaloader.Instaloader()
        user = instaloader.Profile.from_username(L.context, username=username)
        user_info = {"user_name": user.username,
                     "full_name": user.full_name,
                     "biography": user.biography,
                     "followings": user.followees,
                     "followers": user.followers,
                     "media_count": user.mediacount,
                     "profile_pic_url": user.profile_pic_url,
                     "is_business": user.is_business_account,
                     "business_category": user.business_category_name,
                     "is_private": user.is_private}
        return user_info

    def download_profile(self, username):
        L = instaloader.Instaloader()
        user = instaloader.Profile.from_username(L.context, username=username)
        L.download_profilepic(user)

    def download_post(self, link):
        L = instaloader.Instaloader()
        shortcode = re.search(r'^(?:.*\/p\/)([\d\w\-_]+)', link).group(1)
        try:
            post = instaloader.Post.from_shortcode(L.context, shortcode=shortcode)

        except:
            user = 'callme.pyman'
            passwd = '92131349'
            L.login(user=user, passwd=passwd)
            post = instaloader.Post.from_shortcode(L.context, shortcode=shortcode)
        L.download_post(post, target=f'{post.profile}/posts')

    def download_stories(self, target_username, user=None, passwd=None):
        L = instaloader.Instaloader()
        username = target_username
        profile = instaloader.Profile.from_username(L.context, username=username)
        if user is None and passwd is None:
            user = 'callme.pyman'
            passwd = '92131349'
        L.login(user=user, passwd=passwd)
        L.download_stories(userids=[profile.userid], filename_target=f'{profile.username}/stories')

    def download_highlights(self, target_username, user=None, passwd=None):
        L = instaloader.Instaloader()
        username = target_username
        profile = instaloader.Profile.from_username(L.context, username=username)
        if user is None and passwd is None:
            user = 'callme.pyman'
            passwd = '92131349'
        L.login(user=user, passwd=passwd)
        for highlight in L.get_highlights(user=profile):
            for item in highlight.get_items():
                L.download_storyitem(item, target=f"{highlight.owner_username}/highlight/{highlight.title}")
                sleep(1)
