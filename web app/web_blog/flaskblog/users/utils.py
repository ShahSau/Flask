def save_picture(form_picture):
    #convert picture name into a 8 bites long name
    random_hex = secrets.token_hex(8)
    #to save the pics with the same extention as it was uploaded
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    #where to save picture
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    #reducing the pic pixel
    output_size= (125,125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)

    i.save(picture_path)

    return picture_fn

#where reset password should be send
def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='noreply@demo.com', recipients=[user.email])
    msg.body = f'''To reset your password visit the link:
{url_for('reset_token', token=token, _external=True)}
If you didnot make this resquest then discard this email.
    '''
    mail.send(msg)