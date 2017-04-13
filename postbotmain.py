import config
import praw
from datetime import datetime
import time

def login():
    print('logging in...')
    r = praw.Reddit(client_id=config.client_id,
                    client_secret=config.client_secret,
                    user_agent=config.user_agent,
                    username=config.username,
                    password=config.password)
    print('logged in!')
    return r

def create_post(r, title, subreddit):
    post_body = 'for those of you who care to look, I am using a bot to generate a post once per minute. this is to get an accurate (if somewhat unrealistic) ' \
                'way to test a bot I am developing which tracks comments over time. if anyone is reading this, you are more than welcome to use for your own purposes' \
                'but please dont post, as that will generate inaccurate reporting and make it harder to troubleshoot for later generations of potential bot developers, thanks, ' \
                'and happy developing!!'


    mypost = r.subreddit(subreddit).submit(title, post_body , send_replies=False)
    print('successfully posted! \npost-id: {}, post-title: {}, creation time: {}'.format(mypost.id, mypost.title, datetime.fromtimestamp(mypost.created_utc)))
    return mypost

def send_comments(r, submission_id, comment_number):
    newcomment = r.submission(id=submission_id).reply('comment {} / 60'.format(comment_number))
    print(newcomment.id, datetime.fromtimestamp(newcomment.created_utc))


def main():
    r = login()
    mypost = create_post(r, 'creating a timeline', 'test')
    starttime = time.time()
    comment_number = 1
    while comment_number <= 60:
        send_comments(r, mypost.id, comment_number)
        time.sleep(60-((time.time() - starttime) % 60)) #credit to Dave Rove from stackoverflow. this calls send_comments every 60 seconds
        comment_number += 1


main()

