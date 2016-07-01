SOCIAL_AUTH_FACEBOOK_KEY = '1002329286480961'
SOCIAL_AUTH_FACEBOOK_SECRET = 'a150f53cd744e3ef1157241c48799ea6'

SOCIAL_AUTH_FACEBOOK_SCOPE = ['email','public_profile','publish_actions']
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
  'locale': 'ru_RU',
  'fields': 'id, name, email, age_range,picture,gender'
}

SOCIAL_AUTH_FACEBOOK_EXTRA_DATA = [('email','email'),('first_name','first_name'),('last_name','last_name'),('picture','picture'),('gender','gender')]

SOCIAL_AUTH_LINKEDIN_OAUTH2_KEY = '75gwkz5dt9933i'
SOCIAL_AUTH_LINKEDIN_OAUTH2_SECRET = 'YDG7oQpoajMy3QOh'


SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/self_profile/'
SOCIAL_AUTH_LOGIN_URL = '/self_profile/'


SOCIAL_AUTH_PIPELINE = (
    'social.pipeline.social_auth.social_details',
    'social.pipeline.social_auth.social_uid',
    'social.pipeline.social_auth.auth_allowed',
    'social.pipeline.social_auth.social_user',
    'social.pipeline.user.get_username',
    'social.pipeline.user.create_user',
    'social.pipeline.social_auth.associate_by_email',
    'social.pipeline.social_auth.associate_user',
    'social.pipeline.social_auth.load_extra_data',
    'social.pipeline.user.user_details'
)


SOCIAL_AUTH_LINKEDIN_OAUTH2_SCOPE = ['r_basicprofile', 'r_emailaddress']
"""SOCIAL_AUTH_LINKEDIN_FIELD_SELECTORS = [
    'public-profile-url',
    'email-address',
    'interests',
    'skills',
]"""
SOCIAL_AUTH_LINKEDIN_OAUTH2_FIELD_SELECTORS = ['pictureUrl', 'email-address', 'headline', 'industry']
SOCIAL_AUTH_LINKEDIN_OAUTH2_EXTRA_DATA = [('id', 'li_id'),
                               ('firstName', 'first_name'),
                               ('lastName', 'last_name'),
                               ('emailAddress', 'email_address'),
                               ('headline', 'headline'),
                               ('pictureUrl', 'pictureUrl')]
