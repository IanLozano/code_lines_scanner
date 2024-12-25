from flask import (Blueprint, render_template, redirect, url_for, 
                   flash, jsonify, request, send_from_directory, Response)
from models import (db, User, Blog, BlogImage, BlogContents, BlogResources, KeyWords, AdminRole,
                    LikeBlog, VisitorLikeBlog, Subscribe)

from config import (admin_roles, slider_time, website_images,
                    AWS_STORAGE_BUCKET_NAME, AWS_SECRET_ACCESS_KEY, AWS_ACCESS_KEY_ID)
import boto3, io, zipfile, tempfile, random as rd, shutil, os
from flask_login import (current_user, login_required, login_user)


app_blog = Blueprint("blog_section", __name__, template_folder="templates_blog",
                     static_folder="static_blogs",
                     static_url_path="/static_blogs",
                     url_prefix="/holistic_blogs")


COUNT_BLOG_ID = []



BLOG_IMAGE_ID = {}

BLOG_LIST_ID = []
BLOG_FOLDER = "BLOG_FOLDER"

upper_case = [i for i in range(65, 91)] 
lower_case = [i for i in range(97, 123)]
numbers = [str(i) for i in range(10)]
full_case = upper_case + lower_case




@app_blog.route("/blogs/<int:page>", methods = ["GET", "POST"])
def blogs(page=1):
    
    blogs = Blog.query.all()
    blog_claps = {}
    
    blog_items = Blog.query.paginate(1, 6).items
    
    blog_count = len(blog_items)
    
    pages = []
    topics = None
    
    if blogs != []:
        
        
        blogs = Blog.query.all()
     
        for blog in blogs:

            user_claps = blog.liked.count()

            anon_claps = blog.visitor_liked.count()

            count = user_claps + anon_claps

            if count > 0:

                blog_claps.update({blog.id: count})
                
                
    else:
        
        flash("No blogs present yet", "info")
        return redirect(url_for("home"))
        
        
    popularity = {k:v for k, v in sorted(blog_claps.items(), key = lambda item: item[1])[::-1]}
    
    
    x = 0
    blog_dict = {}
    for blog_id in popularity:

        print(blog_id)

        if x < 5:
            blog = Blog.query.filter_by(id = blog_id).first()

            blog_dict.update({blog_id: blog})

            x+= 1


    
    taglist = []
    
    if blogs != []:
        
        #blogs = blogs[::-1]
        
        blogs =Blog.query.paginate(page, 6).items[::-1]
        
        items = len(Blog.query.paginate(page, 6).items)
        
        pages = Blog.query.paginate(page, 6)

        keywords = KeyWords.query.all() 

        if keywords != []:

            check_keys = True

            taglist = list(set([keywords[i].key for i in range(len(keywords))]))

        print("TAG LIST")
        print(taglist)
        
        blogs_topics = Blog.query.all()

        topics = list(set([blogs_topics[i].topic for i in range(len(blogs_topics))]))

        
    
    
    return render_template("blogs.html", title = "blogs",
                           slider_time = slider_time, website_images = website_images,
                           blogs = blogs, 
                           pages = pages, 
                           taglist = taglist, 
                           topics = topics,
                           page = page,
                           items = items,
                           popularity = popularity,
                           blog_dict = blog_dict,
                           blog_count = blog_count)
                           



@app_blog.route("/clapped", methods = ["GET", "POST"])
def clapped():
    
    print("CLAPPED!!!!")
    
    data = request.get_json()
    
    ip_address = request.remote_addr
    
    #LikeBlog, VisitorLikeBlog)
    
    blog_id = int(data["liked"])
    
    COUNT_BLOG_ID.append(blog_id)
    
    
    print("IP ADDRESS", ip_address)
    
    if current_user.is_authenticated:
        
        print("CURRENT_USER ONLINE!!!")
        
        
        
        user_id = current_user.id
        
        
        like_blog = LikeBlog(1, blog_id, user_id)
        
        db.session.add(like_blog)
        db.session.commit()
        
        
    else:
        
        
        visitor_like_blog = VisitorLikeBlog(1,ip_address,  blog_id)
        
        db.session.add(visitor_like_blog)
        db.session.commit()
        
        print("ANON VISITOR!!!")
        
        
    return "blog received a like!"


@app_blog.route("/clap_count", methods = ["GET", "POST"])
def clap_count():
    
    
    blog_id = COUNT_BLOG_ID[-1]
    
    blog = Blog.query.filter_by(id = blog_id).first()

    
    user_claps = blog.liked.count()
    anon_claps = blog.visitor_liked.count()
    
    claps = user_claps + anon_claps

    return jsonify({"total": claps})





@app_blog.route("/one_blog/<string:author>/<int:blog_id>/<string:blog_title>", methods = ["GET", "POST"])
def one_blog(author, blog_id, blog_title):
    
    blog = Blog.query.filter(Blog.id == blog_id).filter(Blog.title == blog_title).first()
    
    blogs = Blog.query.all()
    
    if blogs != []:
        
        recent_blogs = blogs[::-1]
    
    check_keys = False
    keywords = []
    contents = []
    
    author = None
    current_user_id = 0
    updated = False
    admin_user = None
    
    blog_list = None
    
    other_blogs = []
    my_resources = []
            
    check_image = False
    first_page_list = False
    middle_page_list = False
    last_page_list = False

    check_visitor = True
    
    edit_button = False
    blog_resources = False
    
    if blog is None:
        
        flash("This blog does not exist or has been deleted", "info")
        return redirect(url_for("home"))
    
    topic = blog.topic
    
    
    user_claps = blog.liked.count()
    
    anon_claps = blog.visitor_liked.count()
    
    claps = user_claps + anon_claps
    
    if blog.id not in list(BLOG_IMAGE_ID.keys()):
    
        BLOG_IMAGE_ID.update({blog.id: [blog.get_image(), blog]})

        blog_image = BLOG_IMAGE_ID[blog.id]

    else:
        
        blog_image = BLOG_IMAGE_ID[blog.id]
    
    
    print("BLOG IMAGE!!!")
    print(blog_image)
    
    if current_user.is_authenticated:
        
        check_visitor = False
        
   
    if current_user.is_anonymous:
        visitor = True
        check_visitor = True
        
    else:
        
        
        admin_user = AdminRole.query.filter_by(id = blog.admin_id).first()
        visitor = False
        check_visitor = False
        
        current_user_id = current_user.id
        if current_user_id == admin_user.id:
            
            author = True
            
            # EDIT OR DELETE OUR BLOG!
            
            edit_button = True
            
        else:
            
            author = False
            

    other_blogs = Blog.query.filter(Blog.id != blog_id).all()


    BLOG_LIST_ID.append(blog.id)

    blog_data = blog.data.replace("&lt;", "<")

    admin_user = AdminRole.query.filter_by(id = blog.admin_id).first()

    author_user = User.query.filter_by(id = admin_user.user_id).first()


    author_image = author_user.image()

    blogs = Blog.query.all()

    
    


    contents = blog.contents.all()
    
    blog_keys = blog.keys.all()
    
    keywords = KeyWords.query.all() 

    if keywords != []:

        check_keys = True
        
        
        taglist = list(set([keywords[i].key for i in range(len(keywords))]))
        
    print("TAG LIST")
    print(taglist)

    my_resources = blog.resources.all()
    
    if my_resources != []:
        
        blog_resources = True
        
    else:
        
        blog_resources = False

    if blogs != []:

        blog_list = [[blogs[i].title, blogs[i].admin_id, blogs[i].id, 


                  admin_user.first_name,
                  blogs[i].timestamp,
                  admin_user.last_name,
                 admin_user.id
                 ] for i in range(len(blogs))]


    if len(blog.updated) > 0:

        updated = True

    index = None
    final_index = len(blog_list) - 1
    first_index = 0
    page_list = []

    for i in range(len(blog_list)):

        title = blog_list[i][0]
        admin_id = blog_list[i][1]
        blogID = blog_list[i][2]

        if title == blog.title and admin_id == blog.admin_id and blogID == blog.id:

            print(i)
            index = i

            if index == final_index:

                last_page_list = True

                page_list.append(blog_list[final_index-1])

            elif index == first_index:

                first_page_list = True

                page_list.append(blog_list[first_index])
                page_list.append(blog_list[1])

            elif index != first_index and index != final_index:

                middle_page_list = True

                page_list.append(blog_list[i-1])
                page_list.append(blog_list[i])
                page_list.append(blog_list[i +1])

    if request.method == "POST":

        email = request.form.get("email")

        check_email = User.query.filter_by(email = email).first()

        if check_email is not None:

            print("THIS USER ALREADY EXISTS!!!!!")
            flash("This email already exists. If you're registered, please login", "danger")
            return render_template("one_blog.html", title = "one blog",
                          author = author,
                          visitor = visitor,
                          author_user = author_user,
                          blog = blog,
                          current_user_id = current_user_id,
                          blog_data = blog_data,
                           blog_html = blog_data,
                          author_image = author_image,
                          updated = updated,
                          admin_user = admin_user,
                          blog_list = blog_list,
                          page_list = page_list,
                          first_page_list = first_page_list,
                          middle_page_list = middle_page_list,
                          last_page_list = last_page_list,
                          check_visitor = check_visitor,
                           my_resources = my_resources,
                           other_blogs = other_blogs,
                            check_keys = check_keys,
                            keywords = keywords,
                                   contents = contents,
                                   edit_button = edit_button,
                                   blog_image = blog_image,
                                   taglist = taglist,
                                   blog_keys = blog_keys,
                                   topic = topic,
                                   claps = claps,
                                   recent_blogs = recent_blogs,
                                   blog_resources = blog_resources)



        

        else:


            rd.shuffle(full_case)
            suffix = "".join([chr(i) for i in full_case[:4]])

            sub_username = "u_sub_{}".format(suffix)
            sub_last_name = "u_sub_last_{}".format(suffix)
            print(sub_username)



            full_case_numbers = upper_case + lower_case
            rd.shuffle(full_case_numbers)
            pw = [chr(i) for i in full_case_numbers]
            rd.shuffle(numbers)

            temp_pw = "".join(pw[:4] + numbers[:4])

            print("CHECKING EMAIL", email)
            user = User(sub_username, sub_last_name, email, temp_pw, temp_pw)
            db.session.add(user)
            db.session.commit()

            user = User.query.filter(User.email == email).first()

            user.logged_in()
            user.subscribed = True
            db.session.commit()
            
            user = User.query.filter_by(email = email).first()

            subbed = Subscribe(email, blog_id, user.id)
            db.session.add(subbed)
            db.session.commit()

            login_user(user)
            
            check_visitor = False


            flash("Thanks for signing up! Update your username, last name, and password accordingly", "success")
            return redirect(url_for("profile", username = user.username, user_id = user.id))

        
        return render_template("one_blog.html", title = "one blog",
                              author = author,
                              visitor = visitor,
                              author_user = author_user,
                              blog = blog,
                              current_user_id = current_user_id,
                              blog_data = blog_data,
                               blog_html = blog_data,
                              author_image = author_image,
                              updated = updated,
                              admin_user = admin_user,
                              blog_list = blog_list,
                              page_list = page_list,
                              first_page_list = first_page_list,
                              middle_page_list = middle_page_list,
                              last_page_list = last_page_list,
                              check_visitor = check_visitor,
                               my_resources = my_resources,
                               other_blogs = other_blogs,
                                check_keys = check_keys,
                                keywords = keywords,
                               contents = contents,
                               edit_button = edit_button,
                               blog_image = blog_image,
                               taglist = taglist,
                               blog_keys = blog_keys,
                               topic = topic,
                               claps = claps,
                               recent_blogs = recent_blogs,
                               blog_resources = blog_resources)
    


    return render_template("one_blog.html", title = "one blog",
                              author = author,
                              visitor = visitor,
                              author_user = author_user,
                              blog = blog,
                              current_user_id = current_user_id,
                              blog_data = blog_data,
                           blog_html = blog_data,
                              author_image = author_image,
                          updated = updated,
                          admin_user = admin_user,
                          blog_list = blog_list,
                          page_list = page_list,
                              first_page_list = first_page_list,
                              middle_page_list = middle_page_list,
                              last_page_list = last_page_list,
                          check_visitor = check_visitor,
                           my_resources = my_resources,
                           other_blogs = other_blogs,
                            check_keys = check_keys,
                                keywords = keywords,
                           contents = contents,
                           edit_button = edit_button,
                           blog_image = blog_image,
                           taglist = taglist,
                           blog_keys = blog_keys,
                           topic = topic,
                           claps = claps,
                           recent_blogs = recent_blogs,
                           blog_resources = blog_resources)




@app_blog.route("/delete_blog/<string:username>/<int:user_id>/<int:blog_id>", methods = ["GET", "POST"])
@login_required
def delete_blog(username, user_id, blog_id):
    
    user = User.query.filter(User.username == username).filter(User.id == user_id).first()
    
    
    if user.id == current_user.id:
        
        blog = user.blogs.filter(Blog.id == blog_id).first()
        
        
        if blog is not None:

            blog = Blog.query.filter(Blog.user_id == user_id)\
            .filter(Blog.id == blog_id).first()

            db.session.delete(blog)
            db.session.commit()

            print("Blog has been deleted!")
            
        else:
            
            flash("You do not have permission", "danger")
            return redirect(url_for("home"))
            
            
            
    else:
        
        flash("You do not have permission", "danger")
        return redirect(url_for("home"))
        
        
    
    
    flash("Blog has been deleted!", "info")
    return redirect(url_for("home"))

                           
    
    
@app_blog.route("/download_blog_res_file/<int:blog_id>/<int:res_id>", methods = ["GET", "POST"])
def download_blog_res_file(blog_id, res_id):
 


    blog = Blog.query.filter_by(id = blog_id).first()
    
    
    res = blog.resources.filter_by(id = res_id).first()
    
    res.download_count += 1
    db.session.commit()
    
    folder = "blogs/blog_{}/resources/{}".format(*[blog_id, res.file_name])
    
    s3 = boto3.client("s3", region_name = "us-east-1")
    s3_resource = boto3.resource("s3")

    
    file_obj = my_bucket.Object(folder).get()["Body"]

    return Response(

        file_obj,
        mimetype="text/plain",
        headers = {"Content-Disposition": "attachment;filename={}".format(res.file_name)})


    




@app_blog.route("/download_blog_res_zipfile/<int:blog_id>", methods = ["GET", "POST"])
def download_blog_res_zipfile(blog_id):
    
    current_path = os.getcwd()
    
    blog = Blog.query.filter_by(id = blog_id).first()
    print(blog)
    print("DOWNLOAD COUNT!!!")
    print(blog.download_count)
    blog.download_count += 1
    db.session.commit()
    
    
    del_folders = os.listdir(os.getcwd() + "/BLOG_ZIPPED_FOLDER")
    
    
    for folder in del_folders:
        
        zipp_path = os.getcwd() + "/BLOG_ZIPPED_FOLDER/" + folder
        
        print(folder)
        print("DELETING ZIPPING!")
        
        shutil.rmtree(os.getcwd() + "/BLOG_ZIPPED_FOLDER/" + folder)
        
        
    temp_zipp = tempfile.TemporaryDirectory(suffix="_tmp", prefix="zipping_",
                                            dir=current_path + "/BLOG_ZIPPED_FOLDER")
    
    
    s3 = boto3.client("s3", region_name = "us-east-1")
    s3_resource = boto3.resource("s3")
    my_bucket = s3_resource.Bucket(AWS_STORAGE_BUCKET_NAME)
    
    
    paginator = s3.get_paginator("list_objects")
    
    folder = "blogs/blog_{}/resources".format(blog.id)
    
    
    file_list = [page for page in paginator.paginate(Bucket = AWS_STORAGE_BUCKET_NAME)\
                 .search("Contents[?Size >`0`][]")
                 if folder in page["Key"]]
    
    
    for key in file_list:
        
        
        file_name = key["Key"].split("/")[-1]
        
        print(file_name)
        
        file_obj = my_bucket.Object(key["Key"]).get()["Body"]
        
        with open(os.getcwd() + "/" + BLOG_FOLDER + "/" + file_name, "wb") as w:
            
            w.write(file_obj.read())
            
            
    make_zipfile(temp_zipp.name + "/blog_res_{}.zip".format(blog_id),
                 current_path + "/" + BLOG_FOLDER)
    
    try:
        
        for key in file_list:
            
            file_name = key["Key"].split("/")[-1]
            
            file_path = current_path + "/" + BLOG_FOLDER +"/" + file_name
            os.remove(file_path)
            print("TRYY!!")
            print("REMOVED!!!")
            
            
            
    except:
        
        for key in file_list:
            
            file_name = key["Key"].split("/")[-1]
            
            file_path = current_path + "/" + BLOG_FOLDER + "/" + file_name
            os.remove(file_path)
            print("EXCEPT!!!")
            print("REMOVED!!!")

    
    return send_from_directory(temp_zipp.name, "blog_res_{}.zip".format(blog_id),
                               as_attachment = True)










@app_blog.route("/blog_tags/<string:tag_name>", methods = ["GET", "POST"])
def blog_tags(tag_name):
    
    
    return render_template("blog_tags.html", title = "blog tags")



@app_blog.route("/blog_topic/<string:topic_name>", methods = ["GET", "POST"])
def blog_topic(topic_name):
    
    
    return render_template("blog_topic.html", title = "blog topic")























@app_blog.route("/carousel", methods = ["GET", "POST"])
def carousel():
    
    
    
    
    return render_template("carousel.html", title = "carousel",
                           slider_time = slider_time)




























































