from random import choice

images = {
    'slides': ['img/post-slide-1.jpg', 'img/post-slide-2.jpg', 'img/post-slide-3.jpg', 'img/post-slide-4.jpg',
               'img/post-slide-5.jpg', 'img/post-slide-6.jpg'],

    'persons': ['img/person-1.jpg', 'img/person-2.jpg', 'img/person-3.jpg', 'img/person-4.jpg', 'img/person-5.jpg',
                'img/person-6.jpg', 'img/person-7.jpg', 'img/blog/blog-author.jpg', 'img/blog/comments-1.jpg',
                'img/blog/comments-2.jpg', 'img/blog/comments-3.jpg', 'img/blog/comments-4.jpg',
                'img/blog/comments-5.jpg', 'img/blog/comments-6.jpg'],

    'post-landscapes': ['img/post-landscape-1.jpg', 'img/post-landscape-2.jpg', 'img/post-landscape-3.jpg',
                        'img/post-landscape-4.jpg', 'img/post-landscape-5.jpg', 'img/post-landscape-6.jpg',
                        'img/post-landscape-7.jpg', 'img/post-landscape-8.jpg'],

    'post-portraits': ['img/post-portrait-1.jpg', 'img/post-portrait-2.jpg', 'img/post-portrait-3.jpg',
                       'img/post-portrait-4.jpg', 'img/post-portrait-5.jpg', 'img/post-portrait-6.jpg',
                       'img/post-portrait-7.jpg', 'img/post-portrait-8.jpg'],

    'post-sqs': ['img/post-sq-1.jpg', 'img/post-sq-2.jpg', 'img/post-sq-3.jpg', 'img/post-sq-4.jpg',
                 'img/post-sq-5.jpg', 'img/post-sq-6.jpg', 'img/post-sq-7.jpg', 'img/post-sq-8.jpg'],

    'blogs': ['img/blog/blog-1.jpg', 'img/blog/blog-2.jpg', 'img/blog/blog-3.jpg', 'img/blog/blog-4.jpg', 'img/blog/blog-5.jpg',
              'img/blog/blog-6.jpg'],

    'comments': ['img/blog/comments-1.jpg', 'img/blog/comments-2.jpg', 'img/blog/comments-3.jpg',
                 'img/blog/comments-4.jpg', 'img/blog/comments-5.jpg', 'img/blog/comments-6.jpg'],

    'blog_recent': ['img/blog/blog-recent-1.jpg', 'img/blog/blog-recent-2.jpg', 'img/blog/blog-recent-3.jpg',
                    'img/blog/blog-recent-4.jpg', 'img/blog/blog-recent-5.jpg'],

    'blog_author': ['img/blog/blog-author.jpg', 'img/blog/comments-1.jpg', 'img/blog/comments-2.jpg',
                    'img/blog/comments-3.jpg', 'img/blog/comments-4.jpg', 'img/blog/comments-5.jpg',
                    'img/blog/comments-6.jpg']
}


def pick_random_image(key: str):
    """Randomly pick images"""
    return choice(images[key])
