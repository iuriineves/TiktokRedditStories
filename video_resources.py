def create_video_resources(sub ='', num_of_posts = 5):

    from selenium import webdriver
    from selenium.webdriver.common.by import By
    import praw
    import io
    from PIL import Image
    import pyttsx3
    import os

    i = k = r = 0
    letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    videos = []
    titles = []

    engine = pyttsx3.init()
    driver = webdriver.Firefox()

    reddit = praw.Reddit(
        client_id="uWvx6ZAjcJWKuvvj_D_XPQ",
        client_secret="ep8ip4HlWP8I-pmtLK52qxMeyJ5UrA",
        user_agent="Auto Tiktoks 1.0",
    )

    for submission in reddit.subreddit(sub).top(limit=num_of_posts, time_filter = 'day'):
        if not submission.over_18:

            #Entering Reddit
            link = f'https://www.reddit.com/r/{sub}/comments/{submission}'
            driver.get(link)
            element = driver.find_element(By.XPATH, f'//div[@class="subredditvars-r-{sub.lower()}"]')
            driver.execute_script("var element = arguments[0]; element.parentNode.removeChild(element);", element)

            if i == 0:
                #Handle cookies popup
                driver.find_element(By.XPATH, '//form/button[@type="submit"]').click()
            if k == 0:
                #Create folder for resources
                os.mkdir(f'video-resources/{submission.author.name} - {sub}')
                os.mkdir(f'video-resources/{submission.author.name} - {sub}/images')
                os.mkdir(f'video-resources/{submission.author.name} - {sub}/audios')
                folder_name = f'{submission.author.name} - {sub}'

            #Screenshotting and saving the title
            image = driver.find_element(By.XPATH, '//div[@data-test-id="post-content"]/div[@data-adclicklocation="title"]').screenshot_as_png
            imageStream = io.BytesIO(image)
            im = Image.open(imageStream)
            im.save(f'video-resources/{folder_name}/images/! TITLE {submission.author.name} - {sub}.png')

            #Making TTS file
            engine.setProperty("rate", 150)
            title = driver.find_element(By.XPATH, '//div[@data-test-id="post-content"]/div[@data-adclicklocation="title"]').text
            engine.save_to_file(driver.find_element(By.XPATH, '//div[@data-test-id="post-content"]/div[@data-adclicklocation="title"]').text, f'video-resources/{folder_name}/audios/! TITLE TTS {submission.author.name} - {sub}.mp3')
            engine.runAndWait()

            #Screenshotting and saving blocks of text of the story
            for textblock in driver.find_elements(By.XPATH, '//div[@data-test-id="post-content"]/div[@data-adclicklocation="media"]/div/*'):
                image = textblock.screenshot_as_png
                imageStream = io.BytesIO(image)
                im = Image.open(imageStream)
                im.save(f'video-resources/{folder_name}/images/TEXT {letters[k]}{r} {submission.author.name} - {sub}.png')

                #Making TTS file
                engine.setProperty("rate", 200)
                engine.save_to_file(textblock.text, f'video-resources/{folder_name}/audios/TEXT TTS  {letters[k]}{r} {submission.author.name} - {sub}.mp3')
                engine.runAndWait()

                if r < 9:
                    r += 1
                else:
                    r = 0
                    k += 1
            i += 1
            videos.append(f'{folder_name}')
        k = r = 0
    driver.close()

    final_title = f'{title} - #{sub} #redditreadings #redditstories #reddit'
    titles.append(final_title)
    
    print(titles)
    return videos, titles

create_video_resources('TrueOffMyChest', 1)