#!/usr/bin/env python3
"""
MediaServer Database module.
Contains all interactions between the webapp and the queries to the database.
"""

import configparser
import json
import sys
from modules import pg8000

################################################################################
#   Welcome to the database file, where all the query magic happens.
#   My biggest tip is look at the *week 8 lab*.
#   Important information:
#       - If you're getting issues and getting locked out of your database.
#           You may have reached the maximum number of connections.
#           Why? (You're not closing things!) Be careful!
#       - Check things *carefully*.
#       - There may be better ways to do things, this is just for example
#           purposes
#       - ORDERING MATTERS
#           - Unfortunately to make it easier for everyone, we have to ask that
#               your columns are in order. WATCH YOUR SELECTS!! :)
#   Good luck!
#       And remember to have some fun :D
################################################################################

#############################
#                           #
# Database Helper Functions #
#                           #
#############################


#####################################################
#   Database Connect
#   (No need to touch
#       (unless the exception is potatoing))
#####################################################

def database_connect():
    """
    Connects to the database using the connection string.
    If 'None' was returned it means there was an issue connecting to
    the database. It would be wise to handle this ;)
    """
    # Read the config file
    config = configparser.ConfigParser()
    config.read('config.ini')
    if 'database' not in config['DATABASE']:
        config['DATABASE']['database'] = config['DATABASE']['user']

    # Create a connection to the database
    connection = None
    try:
        # Parses the config file and connects using the connect string
        connection = pg8000.connect(database=config['DATABASE']['database'],
                                    user=config['DATABASE']['user'],
                                    password=config['DATABASE']['password'],
                                    host=config['DATABASE']['host'])
    except pg8000.OperationalError as operation_error:
        print("""Error, you haven't updated your config.ini or you have a bad
        connection, please try again. (Update your files first, then check
        internet connection)
        """)
        print(operation_error)
        return None

    # return the connection to use
    return connection


##################################################
# Print a SQL string to see how it would insert  #
##################################################

def print_sql_string(inputstring, params=None):
    """
    Prints out a string as a SQL string parameterized assuming all strings
    """

    if params is not None:
        if params != []:
           inputstring = inputstring.replace("%s","'%s'")
    
    print(inputstring % params)

#####################################################
#   SQL Dictionary Fetch
#   useful for pulling particular items as a dict
#   (No need to touch
#       (unless the exception is potatoing))
#   Expected return:
#       singlerow:  [{col1name:col1value,col2name:col2value, etc.}]
#       multiplerow: [{col1name:col1value,col2name:col2value, etc.}, 
#           {col1name:col1value,col2name:col2value, etc.}, 
#           etc.]
#####################################################

def dictfetchall(cursor,sqltext,params=None):
    """ Returns query results as list of dictionaries."""
    
    result = []
    if (params is None):
        print(sqltext)
    else:
        print("we HAVE PARAMS!")
        print_sql_string(sqltext,params)
    
    cursor.execute(sqltext,params)
    cols = [a[0].decode("utf-8") for a in cursor.description]
    print(cols)
    returnres = cursor.fetchall()
    for row in returnres:
        result.append({a:b for a,b in zip(cols, row)})
    # cursor.close()
    return result

def dictfetchone(cursor,sqltext,params=None):
    """ Returns query results as list of dictionaries."""
    # cursor = conn.cursor()
    result = []
    cursor.execute(sqltext,params)
    cols = [a[0].decode("utf-8") for a in cursor.description]
    returnres = cursor.fetchone()
    result.append({a:b for a,b in zip(cols, returnres)})
    return result



#####################################################
#   Query (1)
#   Login
#####################################################

def check_login(username, password):
    """
    Check that the users information exists in the database.
        - True => return the user data
        - False => return None
    """
    conn = database_connect()
    if(conn is None):
        return None
    cur = conn.cursor()
    try:
        # Try executing the SQL and get from the database
        #########
        # TODO  #  
        #########

        #############################################################################
        # Fill in the SQL below in a manner similar to Wk 08 Lab to log the user in #
        #############################################################################

        sql = """Select *
                 FROM mediaserver.UserAccount
                 Where username=%s
                 AND
                 password=%s;"""
        
        print(username)
        print(password)

        r = dictfetchone(cur,sql,(username,password))
        print(r)
        cur.close()                     # Close the cursor
        conn.close()                    # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Error Invalid Login")
    cur.close()                     # Close the cursor
    conn.close()                    # Close the connection to the db
    return None


#####################################################
#   Is Superuser? - 
#   is this required? we can get this from the login information
#####################################################

def is_superuser(username):
    """
    Check if the user is a superuser.
        - True => Get the departments as a list.
        - False => Return None
    """

    conn = database_connect()
    if(conn is None):
        return None
    cur = conn.cursor()
    try:
        # Try executing the SQL and get from the database
        sql = """SELECT isSuper
                 FROM mediaserver.useraccount
                 WHERE username=%s AND isSuper"""
        print("username is: "+username)
        cur.execute(sql, (username))
        r = cur.fetchone()              # Fetch the first row
        print(r)
        cur.close()                     # Close the cursor
        conn.close()                    # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error:", sys.exc_info()[0])
        raise
    cur.close()                     # Close the cursor
    conn.close()                    # Close the connection to the db
    return None

#####################################################
#   Query (1 b)
#   Get user playlists
#####################################################
def user_playlists(username):
    """
    Check if user has any playlists
        - True -> Return all user playlists
        - False -> Return None
    """

    conn = database_connect()
    if(conn is None):
        return None
    cur = conn.cursor()
    try:
        #########
        # TODO  #  
        #########

        ###############################################################################
        # Fill in the SQL below and make sure you get all the playlists for this user #
        ###############################################################################
        sql = """
        SELECT collection_id, collection_name, Count(media_id)
        FROM mediaserver.MediaCollection Natural Join mediaserver.MediaCollectionContents
        WHERE username = %s
        GROUP BY collection_id, collection_name
        ORDER BY collection_id
        """


        print("username is: "+username)
        r = dictfetchall(cur,sql,(username,))
        print("return val is:")
        print(r)
        cur.close()                     # Close the cursor
        conn.close()                    # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting User Playlists:", sys.exc_info()[0])
        raise
    cur.close()                     # Close the cursor
    conn.close()                    # Close the connection to the db
    return None

#####################################################
#   Query (1 a)
#   Get user podcasts
#####################################################
def user_podcast_subscriptions(username):
    """
    Get user podcast subscriptions.
    """

    conn = database_connect()
    if(conn is None):
        return None
    cur = conn.cursor()
    try:
        #########
        # TODO  #  
        #########

        #################################################################################
        # Fill in the SQL below and get all the podcasts that the user is subscribed to #
        #################################################################################

        sql = """
        SELECT mediaserver.Subscribed_Podcasts.podcast_id,podcast_title,podcast_uri,podcast_last_updated
        FROM mediaserver.Podcast,mediaserver.Subscribed_Podcasts
        WHERE Subscribed_Podcasts.podcast_id = Podcast.podcast_id
        AND Subscribed_Podcasts.username = %s;
        """


        r = dictfetchall(cur,sql,(username,))
        print("return val is:")
        cur.close()                     # Close the cursor
        conn.close()                    # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting Podcast subs:", sys.exc_info()[0])
        raise
    cur.close()                     # Close the cursor
    conn.close()                    # Close the connection to the db
    return None

#####################################################
#   Query (1 c)
#   Get user in progress items
#####################################################
def user_in_progress_items(username):
    """
    Get user in progress items that aren't 100%
    """

    conn = database_connect()
    if(conn is None):
        return None
    cur = conn.cursor()
    try:
        #########
        # TODO  #  
        #########

        ###################################################################################
        # Fill in the SQL below with a way to find all the in progress items for the user #
        ###################################################################################

        sql = """
        SELECT UserMediaConsumption.media_id,play_count AS playcount,progress,lastviewed,storage_location
        FROM mediaserver.UserMediaConsumption, mediaserver.MediaItem
        WHERE UserMediaConsumption.media_id = MediaItem.media_id
        AND 
        username = %s
        ORDER BY lastviewed DESC
        """

        r = dictfetchall(cur,sql,(username,))
        print("return val is:")
        print(r)
        cur.close()                     # Close the cursor
        conn.close()                    # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting User Consumption - Likely no values:", sys.exc_info()[0])
    cur.close()                     # Close the cursor
    conn.close()                    # Close the connection to the db
    return None


#####################################################
#   Get all artists
#####################################################
def get_allartists():
    """
    Get all the artists in your media server
    """

    conn = database_connect()
    if(conn is None):
        return None
    cur = conn.cursor()
    try:
        # Try executing the SQL and get from the database
        sql = """select 
            a.artist_id, a.artist_name, count(amd.md_id) as count
        from 
            mediaserver.artist a left outer join mediaserver.artistmetadata amd on (a.artist_id=amd.artist_id)
        group by a.artist_id, a.artist_name
        order by a.artist_name;"""

        r = dictfetchall(cur,sql)
        print("return val is:")
        print(r)
        cur.close()                     # Close the cursor
        conn.close()                    # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting All Artists:", sys.exc_info()[0])
        raise
    cur.close()                     # Close the cursor
    conn.close()                    # Close the connection to the db
    return None


#####################################################
#   Get all songs
#####################################################
def get_allsongs():
    """
    Get all the songs in your media server
    """

    conn = database_connect()
    if(conn is None):
        return None
    cur = conn.cursor()
    try:
        # Try executing the SQL and get from the database
        sql = """select 
            s.song_id, s.song_title, string_agg(saa.artist_name,',') as artists
        from 
            mediaserver.song s left outer join 
            (mediaserver.Song_Artists sa join mediaserver.Artist a on (sa.performing_artist_id=a.artist_id)
            ) as saa  on (s.song_id=saa.song_id)
        group by s.song_id, s.song_title
        order by s.song_id"""

        r = dictfetchall(cur,sql)
        print("return val is:")
        print(r)
        cur.close()                     # Close the cursor
        conn.close()                    # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting All Songs:", sys.exc_info()[0])
        raise
    cur.close()                     # Close the cursor
    conn.close()                    # Close the connection to the db
    return None


#####################################################
#   Get all podcasts
#####################################################
def get_allpodcasts():
    """
    Get all the podcasts in your media server
    """

    conn = database_connect()
    if(conn is None):
        return None
    cur = conn.cursor()
    try:
        # Try executing the SQL and get from the database
        sql = """select 
                p.*, pnew.count as count  
            from 
                mediaserver.podcast p, 
                (select 
                    p1.podcast_id, count(*) as count 
                from 
                    mediaserver.podcast p1 left outer join mediaserver.podcastepisode pe1 on (p1.podcast_id=pe1.podcast_id) 
                    group by p1.podcast_id) pnew 
            where p.podcast_id = pnew.podcast_id;"""

        r = dictfetchall(cur,sql)
        print("return val is:")
        print(r)
        cur.close()                     # Close the cursor
        conn.close()                    # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting All Podcasts:", sys.exc_info()[0])
        raise
    cur.close()                     # Close the cursor
    conn.close()                    # Close the connection to the db
    return None



#####################################################
#   Get all albums
#####################################################
def get_allalbums():
    """
    Get all the Albums in your media server
    """

    conn = database_connect()
    if(conn is None):
        return None
    cur = conn.cursor()
    try:
        # Try executing the SQL and get from the database
        sql = """select 
                a.album_id, a.album_title, anew.count as count, anew.artists
            from 
                mediaserver.album a, 
                (select 
                    a1.album_id, count(distinct as1.song_id) as count, array_to_string(array_agg(distinct ar1.artist_name),',') as artists
                from 
                    mediaserver.album a1 
			left outer join mediaserver.album_songs as1 on (a1.album_id=as1.album_id) 
			left outer join mediaserver.song s1 on (as1.song_id=s1.song_id)
			left outer join mediaserver.Song_Artists sa1 on (s1.song_id=sa1.song_id)
			left outer join mediaserver.artist ar1 on (sa1.performing_artist_id=ar1.artist_id)
                group by a1.album_id) anew 
            where a.album_id = anew.album_id;"""

        r = dictfetchall(cur,sql)
        print("return val is:")
        print(r)
        cur.close()                     # Close the cursor
        conn.close()                    # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting All Albums:", sys.exc_info()[0])
        raise
    cur.close()                     # Close the cursor
    conn.close()                    # Close the connection to the db
    return None



#####################################################
#   Query (3 a,b c)
#   Get all tvshows
#####################################################
def get_alltvshows():
    """
    Get all the TV Shows in your media server
    """

    conn = database_connect()
    if(conn is None):
        return None
    cur = conn.cursor()
    try:
        #########
        # TODO  #  
        #########

        #############################################################################
        # Fill in the SQL below with a query to get all tv shows and episode counts #
        #############################################################################
        sql = """
        Select tvshow_id, tvshow_title, Count(episode)
        From mediaserver.TVShow left Outer Join mediaserver.TVEpisode using(tvshow_id)
        Group By tvshow_id, tvshow_title
        Order By tvshow_id;
        """

        r = dictfetchall(cur,sql)
        print("return val is:")
        print(r)
        cur.close()                     # Close the cursor
        conn.close()                    # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting All TV Shows:", sys.exc_info()[0])
        raise
    cur.close()                     # Close the cursor
    conn.close()                    # Close the connection to the db
    return None


#####################################################
#   Get all movies
#####################################################
def get_allmovies():
    """
    Get all the Movies in your media server
    """

    conn = database_connect()
    if(conn is None):
        return None
    cur = conn.cursor()
    try:
        # Try executing the SQL and get from the database
        sql = """select 
            m.movie_id, m.movie_title, m.release_year, count(mimd.md_id) as count
        from 
            mediaserver.movie m left outer join mediaserver.mediaitemmetadata mimd on (m.movie_id = mimd.media_id)
        group by m.movie_id, m.movie_title, m.release_year
        order by movie_id;"""

        r = dictfetchall(cur,sql)
        print("return val is:")
        print(r)
        cur.close()                     # Close the cursor
        conn.close()                    # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting All Movies:", sys.exc_info()[0])
        raise
    cur.close()                     # Close the cursor
    conn.close()                    # Close the connection to the db
    return None


#####################################################
#   Get one artist
#####################################################
def get_artist(artist_id):
    """
    Get an artist by their ID in your media server
    """

    conn = database_connect()
    if(conn is None):
        return None
    cur = conn.cursor()
    try:
        # Try executing the SQL and get from the database
        sql = """select *
        from mediaserver.artist a left outer join 
            (mediaserver.artistmetadata natural join mediaserver.metadata natural join mediaserver.MetaDataType) amd
        on (a.artist_id=amd.artist_id)
        where a.artist_id=%s"""

        r = dictfetchall(cur,sql,(artist_id,))
        print("return val is:")
        print(r)
        cur.close()                     # Close the cursor
        conn.close()                    # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting Artist with ID: '"+artist_id+"'", sys.exc_info()[0])
        raise
    cur.close()                     # Close the cursor
    conn.close()                    # Close the connection to the db
    return None


#####################################################
#   Query (2 a,b,c)
#   Get one song
#####################################################
def get_song(song_id):
    """
    Get a song by their ID in your media server
    """

    conn = database_connect()
    if(conn is None):
        return None
    cur = conn.cursor()
    try:
        #########
        # TODO  #  
        #########

        #############################################################################
        # Fill in the SQL below with a query to get all information about a song    #
        # and the artists that performed it                                         #
        #############################################################################
        sql = """
        Select song_title, string_agg(artist_name, ',') as "artists", length
        From mediaserver.Song Left Outer Join (mediaserver.Song_Artists Join mediaserver.Artist on (performing_artist_id = artist_id)) using(song_id)
        Where song_id = %s
        Group By song_title, length;
        """

        r = dictfetchall(cur,sql,(song_id,))
        print("return val is:")
        print(r)
        cur.close()                     # Close the cursor
        conn.close()                    # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting All Songs:", sys.exc_info()[0])
        raise
    cur.close()                     # Close the cursor
    conn.close()                    # Close the connection to the db
    return None

#####################################################
#   Query (2 d)
#   Get metadata for one song
#####################################################
def get_song_metadata(song_id):
    """
    Get the meta for a song by their ID in your media server
    """

    conn = database_connect()
    if(conn is None):
        return None
    cur = conn.cursor()
    try:
        #########
        # TODO  #  
        #########

        #############################################################################
        # Fill in the SQL below with a query to get all metadata about a song       #
        #############################################################################

        sql = """
        Select md_value, md_type_name, md_id
        From mediaserver.Song Join mediaserver.MediaItemMetaData On(song_id = media_id) Join mediaserver.MetaData Using(md_id) Join mediaserver.MetaDataType Using(md_type_id)
        Where song_id = %s;
        """

        r = dictfetchall(cur,sql,(song_id,))
        print("return val is:")
        print(r)
        cur.close()                     # Close the cursor
        conn.close()                    # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting song metadata for ID: "+song_id, sys.exc_info()[0])
        raise
    cur.close()                     # Close the cursor
    conn.close()                    # Close the connection to the db
    return None

#####################################################
#   Query (6 a,b,c,d,e)
#   Get one podcast and return all metadata associated with it
#####################################################
def get_podcast(podcast_id):
    """
    Get a podcast by their ID in your media server
    """

    conn = database_connect()
    if(conn is None):
        return None
    cur = conn.cursor()
    try:
        #########
        # TODO  #  
        #########

        #############################################################################
        # Fill in the SQL below with a query to get all information about a podcast #
        # including all metadata associated with it                                 #
        #############################################################################
        sql = """
        Select podcast_id, podcast_title, podcast_uri, podcast_last_updated, md_value, md_type_name, md_id
        From mediaserver.Podcast Left Outer Join (mediaserver.PodcastMetaData Natural Join mediaserver.MetaData Natural Join mediaserver.MetaDataType) Using(podcast_id)
        Where podcast_id = %s;
        """

        r = dictfetchall(cur,sql,(podcast_id,))
        print("return val is:")
        print(r)
        cur.close()                     # Close the cursor
        conn.close()                    # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting Podcast with ID: "+podcast_id, sys.exc_info()[0])
        raise
    cur.close()                     # Close the cursor
    conn.close()                    # Close the connection to the db
    return None

#####################################################
#   Query (6 f)
#   Get all podcast eps for one podcast
#####################################################
def get_all_podcasteps_for_podcast(podcast_id):
    """
    Get all podcast eps for one podcast by their podcast ID in your media server
    """

    conn = database_connect()
    if(conn is None):
        return None
    cur = conn.cursor()
    try:
        #########
        # TODO  #  
        #########

        #############################################################################
        # Fill in the SQL below with a query to get all information about all       #
        # podcast episodes in a podcast                                             #
        #############################################################################
        
        sql = """
        Select media_id, podcast_episode_title, podcast_episode_uri, podcast_episode_published_date, podcast_episode_length
        From mediaserver.PodcastEpisode
        Where podcast_id = %s
        Order By podcast_episode_published_date DESC;
        """

        r = dictfetchall(cur,sql,(podcast_id,))
        print("return val is:")
        print(r)
        cur.close()                     # Close the cursor
        conn.close()                    # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting All Podcast Episodes for Podcast with ID: "+podcast_id, sys.exc_info()[0])
        raise
    cur.close()                     # Close the cursor
    conn.close()                    # Close the connection to the db
    return None


#####################################################
#   Query (7 a,b,c,d,e,f)
#   Get one podcast ep and associated metadata
#####################################################
def get_podcastep(podcastep_id):
    """
    Get a podcast ep by their ID in your media server
    """

    conn = database_connect()
    if(conn is None):
        return None
    cur = conn.cursor()
    try:
        #########
        # TODO  #  
        #########

        #############################################################################
        # Fill in the SQL below with a query to get all information about a         #
        # podcast episodes and it's associated metadata                             #
        #############################################################################
        sql = """
        Select media_id, podcast_episode_title, podcast_episode_uri, podcast_episode_published_date, podcast_episode_length, md_value, md_type_name
        From mediaserver.PodcastEpisode Left Outer Join (mediaserver.MediaItemMetaData Natural Join mediaserver.MetaData Natural Join mediaserver.MetaDataType) Using(media_id)
        Where media_id = %s;
        """

        r = dictfetchall(cur,sql,(podcastep_id,))
        print("return val is:")
        print(r)
        cur.close()                     # Close the cursor
        conn.close()                    # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting Podcast Episode with ID: "+podcastep_id, sys.exc_info()[0])
        raise
    cur.close()                     # Close the cursor
    conn.close()                    # Close the connection to the db
    return None


#####################################################
#   Query (5 a,b)
#   Get one album
#####################################################
def get_album(album_id):
    """
    Get an album by their ID in your media server
    """

    conn = database_connect()
    if(conn is None):
        return None
    cur = conn.cursor()
    try:
        #########
        # TODO  #  
        #########

        #############################################################################
        # Fill in the SQL below with a query to get all information about an album  #
        # including all relevant metadata                                           #
        #############################################################################
        sql = """
        select album_title, md_value, md_type_name, md_id
        from mediaserver.Album left outer join (mediaserver.AlbumMetaData Natural Join mediaserver.MetaData Natural Join mediaserver.MetaDataType) Using (album_id)
        where album_id = %s;
        """

        r = dictfetchall(cur,sql,(album_id,))
        print("return val is:")
        print(r)
        cur.close()                     # Close the cursor
        conn.close()                    # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting Albums with ID: "+album_id, sys.exc_info()[0])
        raise
    cur.close()                     # Close the cursor
    conn.close()                    # Close the connection to the db
    return None


#####################################################
#   Query (5 d)
#   Get all songs for one album
#####################################################
def get_album_songs(album_id):
    """
    Get all songs for an album by the album ID in your media server
    """

    conn = database_connect()
    if(conn is None):
        return None
    cur = conn.cursor()
    try:
        #########
        # TODO  #  
        #########

        #############################################################################
        # Fill in the SQL below with a query to get all information about all       #
        # songs in an album, including their artists                                #
        #############################################################################
        sql = """
        select S.song_id, song_title, string_agg(T.artist_name,',') as artists
        from mediaserver.Album A left outer join mediaserver.Album_Songs S on (A.album_id = S.album_id)
        left outer join mediaserver.Song_Artists R on (S.song_id = R.song_id)
        left outer join mediaserver.Artist T on (R.performing_artist_id = T.artist_id)
        left outer join mediaserver.Song O on (S.song_id = O.song_id)
        where A.album_id = %s
		group by S.song_id, song_title
		order by S.song_id;
        """

        r = dictfetchall(cur,sql,(album_id,))
        print("return val is:")
        print(r)
        cur.close()                     # Close the cursor
        conn.close()                    # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting Albums songs with ID: "+album_id, sys.exc_info()[0])
        raise
    cur.close()                     # Close the cursor
    conn.close()                    # Close the connection to the db
    return None


#####################################################
#   Query (5 c)
#   Get all genres for one album
#####################################################
def get_album_genres(album_id):
    """
    Get all genres for an album by the album ID in your media server
    """

    conn = database_connect()
    if(conn is None):
        return None
    cur = conn.cursor()
    try:
        #########
        # TODO  #  
        #########

        #############################################################################
        # Fill in the SQL below with a query to get all information about all       #
        # genres in an album (based on all the genres of the songs in that album)   #
        #############################################################################
        sql = """
        Select Distinct md_value as songgenres, md_id
From mediaserver.Album Left Outer Join mediaserver.Album_Songs Using(album_id) Left Outer Join (mediaserver.MediaItemMetaData Natural Join mediaserver.metadata Natural Join mediaserver.MetaDataType) On(song_id = media_id)
Where album_id = %s AND md_type_id = 1
        """

        r = dictfetchall(cur,sql,(album_id,))
        print("return val is:")
        print(r)
        cur.close()                     # Close the cursor
        conn.close()                    # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting Albums genres with ID: "+album_id, sys.exc_info()[0])
        raise
    cur.close()                     # Close the cursor
    conn.close()                    # Close the connection to the db
    return None

#####################################################
#   Query (10)
#   May require the addition of SQL to multiple 
#   functions and the creation of a new function to
#   determine what type of genre is being provided
#   You may have to look at the hard coded values
#   in the sampledata to make your choices
#####################################################
def get_genre_type(genre_id):
    """
    Get all songs for a particular song_genre ID in your media server
    """
    conn = database_connect()
    if(conn is None):
        return None
    cur = conn.cursor()
    try:
        #########
        # TODO  #  
        #########

        #############################################################################
        # Fill in the SQL below with a query to get all information about all       #
        # songs which belong to a particular genre_id                               #
        #############################################################################
        sql = """
        Select Distinct md_type_id, md_value
        From mediaserver.MediaItemMetaData Natural Join mediaserver.MetaData Natural Join mediaserver.MetaDataType
        Where md_id = %s;
        """

        r = dictfetchall(cur,sql,(genre_id,))
        print("return val is:")
        print(r)
        cur.close()                     # Close the cursor
        conn.close()                    # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting Genre Type with Genre ID: "+genre_id, sys.exc_info()[0])
        raise
    cur.close()                     # Close the cursor
    conn.close()                    # Close the connection to the db
    return None

#####################################################
#   Query (10)
#   Get all songs for one song_genre
#####################################################

def get_genre_songs(genre_id):
    """
    Get all songs for a particular song_genre ID in your media server
    """
    conn = database_connect()
    if(conn is None):
        return None
    cur = conn.cursor()
    try:
        #########
        # TODO  #  
        #########

        #############################################################################
        # Fill in the SQL below with a query to get all information about all       #
        # songs which belong to a particular genre_id                               #
        #############################################################################
        sql = """
        Select media_id as item_id, song_title as item_title, 'Song' as item_type
        From mediaserver.Song Left Outer Join (mediaserver.MediaItemMetaData Natural Join mediaserver.MetaData Natural Join mediaserver.MetaDataType) on(song_id=media_id)
        Where md_type_id = 1 And md_id = %s;
        """

        r = dictfetchall(cur,sql,(genre_id,))
        print("return val is:")
        print(r)
        cur.close()                     # Close the cursor
        conn.close()                    # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting Songs with Genre ID: "+genre_id, sys.exc_info()[0])
        raise
    cur.close()                     # Close the cursor
    conn.close()                    # Close the connection to the db
    return None

#####################################################
#   Query (10)
#   Get all podcasts for one podcast_genre
#####################################################
def get_genre_podcasts(genre_id):
    """
    Get all podcasts for a particular podcast_genre ID in your media server
    """
    conn = database_connect()
    if(conn is None):
        return None
    cur = conn.cursor()
    try:
        #########
        # TODO  #  
        #########

        #############################################################################
        # Fill in the SQL below with a query to get all information about all       #
        # podcasts which belong to a particular genre_id                            #
        #############################################################################
        sql = """
        Select podcast_id as item_id, podcast_title as item_title, 'Podcast' as item_type
        From mediaserver.podcast Left Outer Join (mediaserver.PodcastMetaData Natural Join mediaserver.MetaData Natural Join mediaserver.MetaDataType) Using(podcast_id)
        Where md_type_id = 6 And md_id = %s;
        """

        r = dictfetchall(cur,sql,(genre_id,))
        print("return val is:")
        print(r)
        cur.close()                     # Close the cursor
        conn.close()                    # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting Podcasts with Genre ID: "+genre_id, sys.exc_info()[0])
        raise
    cur.close()                     # Close the cursor
    conn.close()                    # Close the connection to the db
    return None

#####################################################
#   Query (10)
#   Get all movies and tv shows for one film_genre
#####################################################
def get_genre_movies_and_shows(genre_id):
    """
    Get all movies and tv shows for a particular film_genre ID in your media server
    """
    conn = database_connect()
    if(conn is None):
        return None
    cur = conn.cursor()
    try:
        #########
        # TODO  #  
        #########

        #############################################################################
        # Fill in the SQL below with a query to get all information about all       #
        # movies and tv shows which belong to a particular genre_id                 #
        #############################################################################
        sql = """
        Select movie_id as item_id, movie_title as item_title, 'Movie' as item_type
        From mediaserver.movie Left Outer Join (mediaserver.MediaItemMetaData Natural Join mediaserver.MetaData Natural Join mediaserver.MetaDataType) on(movie_id = media_id)
        Where md_type_id = 2 And md_id = %s
        Union
        Select tvshow_id as item_id, tvshow_title as item_title, 'TV Show' as item_type
        From mediaserver.tvshow Left Outer Join (mediaserver.TVShowMetaData Natural Join mediaserver.MetaData Natural Join mediaserver.MetaDataType) Using(tvshow_id)
        Where md_type_id = 2 And md_id = %s;
        """

        r = dictfetchall(cur,sql,(genre_id,genre_id))
        print("return val is:")
        print(r)
        cur.close()                     # Close the cursor
        conn.close()                    # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting Movies and tv shows with Genre ID: "+genre_id, sys.exc_info()[0])
        raise
    cur.close()                     # Close the cursor
    conn.close()                    # Close the connection to the db
    return None



#####################################################
#   Query (4 a,b)
#   Get one tvshow
#####################################################
def get_tvshow(tvshow_id):
    """
    Get one tvshow in your media server
    """

    conn = database_connect()
    if(conn is None):
        return None
    cur = conn.cursor()
    try:
        #########
        # TODO  #  
        #########

        #############################################################################
        # Fill in the SQL below with a query to get all information about a tv show #
        # including all relevant metadata       #
        #############################################################################
        sql = """
        Select tvshow_id, md_value, md_type_name, md_id
        From mediaserver.tvshow Left Outer Join (mediaserver.tvshowmetadata Natural Join mediaserver.metadata Natural Join mediaserver.metadatatype) Using(tvshow_id)
        where tvshow_id = %s;
        """

        r = dictfetchall(cur,sql,(tvshow_id,))
        print("return val is:")
        print(r)
        cur.close()                     # Close the cursor
        conn.close()                    # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting All TV Shows:", sys.exc_info()[0])
        raise
    cur.close()                     # Close the cursor
    conn.close()                    # Close the connection to the db
    return None


#####################################################
#   Query (4 c)
#   Get all tv show episodes for one tv show
#####################################################
def get_all_tvshoweps_for_tvshow(tvshow_id):
    """
    Get all tvshow episodes for one tv show in your media server
    """

    conn = database_connect()
    if(conn is None):
        return None
    cur = conn.cursor()
    try:
        #########
        # TODO  #  
        #########

        #############################################################################
        # Fill in the SQL below with a query to get all information about all       #
        # tv episodes in a tv show                                                  #
        #############################################################################
        sql = """
        Select media_id, tvshow_episode_title, season, episode, air_date
        From mediaserver.tvepisode
        Where tvshow_id = %s
        Order By season DESC, episode DESC;
        """

        r = dictfetchall(cur,sql,(tvshow_id,))
        print("return val is:")
        print(r)
        cur.close()                     # Close the cursor
        conn.close()                    # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting All TV Shows:", sys.exc_info()[0])
        raise
    cur.close()                     # Close the cursor
    conn.close()                    # Close the connection to the db
    return None


#####################################################
#   Get one tvshow episode
#####################################################
def get_tvshowep(tvshowep_id):
    """
    Get one tvshow episode in your media server
    """

    conn = database_connect()
    if(conn is None):
        return None
    cur = conn.cursor()
    try:
        # Try executing the SQL and get from the database
        sql = """select * 
        from mediaserver.TVEpisode te left outer join 
            (mediaserver.mediaitemmetadata natural join mediaserver.metadata natural join mediaserver.MetaDataType) temd
            on (te.media_id=temd.media_id)
        where te.media_id = %s"""

        r = dictfetchall(cur,sql,(tvshowep_id,))
        print("return val is:")
        print(r)
        cur.close()                     # Close the cursor
        conn.close()                    # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting All TV Shows:", sys.exc_info()[0])
        raise
    cur.close()                     # Close the cursor
    conn.close()                    # Close the connection to the db
    return None


#####################################################

#   Get one movie
#####################################################
def get_movie(movie_id):
    """
    Get one movie in your media server
    """

    conn = database_connect()
    if(conn is None):
        return None
    cur = conn.cursor()
    try:
        # Try executing the SQL and get from the database
        sql = """select *
        from mediaserver.movie m left outer join 
            (mediaserver.mediaitemmetadata natural join mediaserver.metadata natural join mediaserver.MetaDataType) mmd
        on (m.movie_id=mmd.media_id)
        where m.movie_id=%s;"""

        r = dictfetchall(cur,sql,(movie_id,))
        print("return val is:")
        print(r)
        cur.close()                     # Close the cursor
        conn.close()                    # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting All Movies:", sys.exc_info()[0])
        raise
    cur.close()                     # Close the cursor
    conn.close()                    # Close the connection to the db
    return None


#####################################################
#   Find all matching tvshows
#####################################################
def find_matchingtvshows(searchterm):
    """
    Get all the matching TV Shows in your media server
    """

    conn = database_connect()
    if(conn is None):
        return None
    cur = conn.cursor()
    try:
        # Try executing the SQL and get from the database
        sql = """
            select 
                t.*, tnew.count as count  
            from 
                mediaserver.tvshow t, 
                (select 
                    t1.tvshow_id, count(te1.media_id) as count 
                from 
                    mediaserver.tvshow t1 left outer join mediaserver.TVEpisode te1 on (t1.tvshow_id=te1.tvshow_id) 
                    group by t1.tvshow_id) tnew 
            where t.tvshow_id = tnew.tvshow_id and lower(tvshow_title) ~ lower(%s)
            order by t.tvshow_id;"""

        r = dictfetchall(cur,sql,(searchterm,))
        print("return val is:")
        print(r)
        cur.close()                     # Close the cursor
        conn.close()                    # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting All TV Shows:", sys.exc_info()[0])
        raise
    cur.close()                     # Close the cursor
    conn.close()                    # Close the connection to the db
    return None


#####################################################
#   Query (9)
#   Find all matching Movies
#####################################################
def find_matchingmovies(searchterm):
    """
    Get all the matching Movies in your media server
    """

    conn = database_connect()
    if(conn is None):
        return None
    cur = conn.cursor()
    try:
        #########
        # TODO  #  
        #########

        #############################################################################
        # Fill in the SQL below with a query to get all information about movies    #
        # that match a given search term                                            #
        #############################################################################
        sql = """
        select movie_id, movie_title, release_year, count(md_value) as count
        from mediaserver.Movie M left outer join mediaserver.VideoMedia V on (M.movie_id = V.media_id)
        natural join mediaserver.MediaItem
        natural join mediaserver.MediaItemMetaData
        natural join mediaserver.MetaData
        natural join mediaserver.MetaDataType
		 where lower(M.movie_title) ~ lower(%s)
        group by movie_id, movie_title
       ;
        """

        r = dictfetchall(cur,sql,(searchterm,))
        print("return val is:")
        print(r)
        cur.close()                     # Close the cursor
        conn.close()                    # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting All TV Shows:", sys.exc_info()[0])
        raise
    cur.close()                     # Close the cursor
    conn.close()                    # Close the connection to the db
    return None



#####################################################
#   Add a new Movie
#####################################################
def add_movie_to_db(title,release_year,description,storage_location,genre):
    """
    Add a new Movie to your media server
    """
    conn = database_connect()
    if(conn is None):
        return None
    cur = conn.cursor()
    try:
        # Try executing the SQL and get from the database
        sql = """
        SELECT 
            mediaserver.addMovie(
                %s,%s,%s,%s,%s);
        """

        cur.execute(sql,(storage_location,description,title,release_year,genre))
        conn.commit()                   # Commit the transaction
        r = cur.fetchone()
        print("return val is:")
        print(r)
        cur.close()                     # Close the cursor
        conn.close()                    # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error adding a movie:", sys.exc_info()[0])
        raise
    cur.close()                     # Close the cursor
    conn.close()                    # Close the connection to the db
    return None

#####################################################
#   Query (8)
#   Add a new Song
#####################################################
def add_song_to_db(songlocation,songdescription,songlength,artistid,genre_id,songtitle):
    """
    Get all the matching Movies in your media server
    """
    #########
    # TODO  #  
    #########
    conn = database_connect()
    if(conn is None):
        return None
    cur = conn.cursor()
    try:
        # Try executing the SQL and get from the database
        sql = """
        SELECT 
            mediaserver.addSong(
                %s,%s,%s,%s,%s,%s);
        """

        cur.execute(sql,(songlocation,songdescription,songtitle,songlength,genre_id,artistid,))
        conn.commit()                   # Commit the transaction
        r = cur.fetchone()
        print("return val is:")
        print(r)
        cur.close()                     # Close the cursor
        conn.close()                    # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error adding a movie:", sys.exc_info()[0])
        raise
    cur.close()                     # Close the cursor
    conn.close()                    # Close the connection to the db
    return None
    #############################################################################
    # Fill in the Function  with a query and management for how to add a new    #
    # song to your media server. Make sure you manage all constraints           #
    #############################################################################
def get_all_song_genres():
    conn = database_connect()
    if(conn is None):
        return None
    cur = conn.cursor()
    try:
        # Try executing the SQL and get from the database
        sql = """
            Select *
            From mediaserver.metadata natural join mediaserver.MetaDataType
            Where md_type_id = 1;"""

        r = dictfetchall(cur,sql)
        print("return val is:")
        print(r)
        cur.close()                     # Close the cursor
        conn.close()                    # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting All Song Genres:", sys.exc_info()[0])
        raise
    cur.close()                     # Close the cursor
    conn.close()                    # Close the connection to the db
    return None



#####################################################
#   Get last Movie
#####################################################
def get_last_movie():
    """
    Get all the latest entered movie in your media server
    """

    conn = database_connect()
    if(conn is None):
        return None
    cur = conn.cursor()
    try:
        # Try executing the SQL and get from the database
        sql = """
        select max(movie_id) as movie_id from mediaserver.movie"""

        r = dictfetchone(cur,sql)
        print("return val is:")
        print(r)
        cur.close()                     # Close the cursor
        conn.close()                    # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error adding a movie:", sys.exc_info()[0])
        raise
    cur.close()                     # Close the cursor
    conn.close()                    # Close the connection to the db
    return None

def get_last_song():
    """
    Get all the latest entered song in your media server
    """

    conn = database_connect()
    if(conn is None):
        return None
    cur = conn.cursor()
    try:
        # Try executing the SQL and get from the database
        sql = """
        select max(song_id) as song_id from mediaserver.song"""

        r = dictfetchone(cur,sql)
        print("return val is:")
        print(r)
        cur.close()                     # Close the cursor
        conn.close()                    # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error adding a song:", sys.exc_info()[0])
        raise
    cur.close()                     # Close the cursor
    conn.close()                    # Close the connection to the db
    return None

#  FOR MARKING PURPOSES ONLY
#  DO NOT CHANGE

def to_json(fn_name, ret_val):
    """
    TO_JSON used for marking; Gives the function name and the
    return value in JSON.
    """
    return {'function': fn_name, 'res': json.dumps(ret_val)}

# =================================================================
# =================================================================

#####################################################
#   Multi-Term Search
#####################################################
def movie_multi_term_search(movie_title, genre, release_year, release_year_sign):
    conn = database_connect()
    if(conn is None):
        return None
    cur = conn.cursor()
    try:
        # Try executing the SQL and get from the database
        if(release_year.isnumeric() == False):
            return None

        if release_year_sign == '>':
            sql = """
                Select movie_id, movie_title, release_year, Count(md_value)
                From mediaserver.Movie Left Outer Join (mediaserver.mediaitemmetadata natural join mediaserver.metadata natural join mediaserver.MetaDataType) On(movie_id=media_id)
                Where movie_id in (Select Distinct movie_id
                					From mediaserver.Movie Left Outer Join (mediaserver.mediaitemmetadata natural join mediaserver.metadata natural join mediaserver.MetaDataType) On(movie_id=media_id)
                					Where lower(movie_title) ~ lower(%s) AND release_year > %s AND lower(md_value) ~ lower(%s) AND md_type_id = 2)
                Group By movie_id, movie_title, release_year
                Order By movie_id;"""
        elif release_year_sign == '<':
            sql = """
                Select movie_id, movie_title, release_year, Count(md_value)
                From mediaserver.Movie Left Outer Join (mediaserver.mediaitemmetadata natural join mediaserver.metadata natural join mediaserver.MetaDataType) On(movie_id=media_id)
                Where movie_id in (Select Distinct movie_id
                                    From mediaserver.Movie Left Outer Join (mediaserver.mediaitemmetadata natural join mediaserver.metadata natural join mediaserver.MetaDataType) On(movie_id=media_id)
                                    Where lower(movie_title) ~ lower(%s) AND release_year < %s AND lower(md_value) ~ lower(%s) AND md_type_id = 2)
                Group By movie_id, movie_title, release_year
                Order By movie_id;"""
        else:
            sql = """
                Select movie_id, movie_title, release_year, Count(md_value)
                From mediaserver.Movie Left Outer Join (mediaserver.mediaitemmetadata natural join mediaserver.metadata natural join mediaserver.MetaDataType) On(movie_id=media_id)
                Where movie_id in (Select Distinct movie_id
                                    From mediaserver.Movie Left Outer Join (mediaserver.mediaitemmetadata natural join mediaserver.metadata natural join mediaserver.MetaDataType) On(movie_id=media_id)
                                    Where lower(movie_title) ~ lower(%s) AND release_year = %s AND lower(md_value) ~ lower(%s) AND md_type_id = 2)
                Group By movie_id, movie_title, release_year
                Order By movie_id;"""
        r = dictfetchall(cur,sql,(movie_title,release_year,genre,))
        print("return val is:")
        print(r)
        cur.close()                     # Close the cursor
        conn.close()                    # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting All Movies:", sys.exc_info()[0])
        raise
    cur.close()                     # Close the cursor
    conn.close()                    # Close the connection to the db
    return None

def song_multi_term_search(song_title,song_genre,song_length,song_length_sign,song_artist):
    conn = database_connect()
    if(conn is None):
        return None
    cur = conn.cursor()
    try:
        # Try executing the SQL and get from the database
        if(song_length.isnumeric() == False):
            return None            

        if song_length_sign == '=':
            if song_genre != '' and song_artist != '':
                sql = """
                    Select song_id, song_title, array_to_string(array_agg(distinct artist_name),',') as artists
                    From mediaserver.song Left Outer Join mediaserver.Song_Artists Using(song_id) Left Outer Join mediaserver.Artist On(performing_artist_id=artist_id)
                    Where lower(song_title) ~ lower(%s) And length = %s And lower(artist_name) ~ lower(%s)
                    And song_id in (Select song_id
                    				From mediaserver.song Left Outer Join (mediaserver.mediaitemmetadata natural join mediaserver.metadata natural join mediaserver.MetaDataType) On(song_id=media_id)
                    				Where lower(md_value) ~ lower(%s) And md_type_id = 1)
                    Group By song_id, song_title
                    Order By song_id;"""
            elif song_genre != '':
                sql = """
                    Select song_id, song_title, array_to_string(array_agg(distinct artist_name),',') as artists
                    From mediaserver.song Left Outer Join mediaserver.Song_Artists Using(song_id) Left Outer Join mediaserver.Artist On(performing_artist_id=artist_id)
                    Where lower(song_title) ~ lower(%s) And length = %s
                    And song_id in (Select song_id
                                    From mediaserver.song Left Outer Join (mediaserver.mediaitemmetadata natural join mediaserver.metadata natural join mediaserver.MetaDataType) On(song_id=media_id)
                                    Where lower(md_value) ~ lower(%s) And md_type_id = 1)
                    Group By song_id, song_title
                    Order By song_id;"""
            elif song_artist != '':
                sql = """
                    Select song_id, song_title, array_to_string(array_agg(distinct artist_name),',') as artists
                    From mediaserver.song Left Outer Join mediaserver.Song_Artists Using(song_id) Left Outer Join mediaserver.Artist On(performing_artist_id=artist_id)
                    Where lower(song_title) ~ lower(%s) And length = %s And lower(artist_name) ~ lower(%s)
                    Group By song_id, song_title
                    Order By song_id;"""
            else:
                sql = """
                    Select song_id, song_title, array_to_string(array_agg(distinct artist_name),',') as artists
                    From mediaserver.song Left Outer Join mediaserver.Song_Artists Using(song_id) Left Outer Join mediaserver.Artist On(performing_artist_id=artist_id)
                    Where lower(song_title) ~ lower(%s) And length = %s
                    Group By song_id, song_title
                    Order By song_id;"""
        elif song_length_sign == '>':
            if song_genre != '' and song_artist != '':
                sql = """
                    Select song_id, song_title, array_to_string(array_agg(distinct artist_name),',') as artists
                    From mediaserver.song Left Outer Join mediaserver.Song_Artists Using(song_id) Left Outer Join mediaserver.Artist On(performing_artist_id=artist_id)
                    Where lower(song_title) ~ lower(%s) And length > %s And lower(artist_name) ~ lower(%s)
                    And song_id in (Select song_id
                                    From mediaserver.song Left Outer Join (mediaserver.mediaitemmetadata natural join mediaserver.metadata natural join mediaserver.MetaDataType) On(song_id=media_id)
                                    Where lower(md_value) ~ lower(%s) And md_type_id = 1)
                    Group By song_id, song_title
                    Order By song_id;"""
            elif song_genre != '':
                sql = """
                    Select song_id, song_title, array_to_string(array_agg(distinct artist_name),',') as artists
                    From mediaserver.song Left Outer Join mediaserver.Song_Artists Using(song_id) Left Outer Join mediaserver.Artist On(performing_artist_id=artist_id)
                    Where lower(song_title) ~ lower(%s) And length > %s
                    And song_id in (Select song_id
                                    From mediaserver.song Left Outer Join (mediaserver.mediaitemmetadata natural join mediaserver.metadata natural join mediaserver.MetaDataType) On(song_id=media_id)
                                    Where lower(md_value) ~ lower(%s) And md_type_id = 1)
                    Group By song_id, song_title
                    Order By song_id;"""
            elif song_artist != '':
                sql = """
                    Select song_id, song_title, array_to_string(array_agg(distinct artist_name),',') as artists
                    From mediaserver.song Left Outer Join mediaserver.Song_Artists Using(song_id) Left Outer Join mediaserver.Artist On(performing_artist_id=artist_id)
                    Where lower(song_title) ~ lower(%s) And length > %s And lower(artist_name) ~ lower(%s)
                    Group By song_id, song_title
                    Order By song_id;"""
            else:
                sql = """
                    Select song_id, song_title, array_to_string(array_agg(distinct artist_name),',') as artists
                    From mediaserver.song Left Outer Join mediaserver.Song_Artists Using(song_id) Left Outer Join mediaserver.Artist On(performing_artist_id=artist_id)
                    Where lower(song_title) ~ lower(%s) And length > %s
                    Group By song_id, song_title
                    Order By song_id;"""
        else:
            if song_genre != '' and song_artist != '':
                sql = """
                    Select song_id, song_title, array_to_string(array_agg(distinct artist_name),',') as artists
                    From mediaserver.song Left Outer Join mediaserver.Song_Artists Using(song_id) Left Outer Join mediaserver.Artist On(performing_artist_id=artist_id)
                    Where lower(song_title) ~ lower(%s) And length < %s And lower(artist_name) ~ lower(%s)
                    And song_id in (Select song_id
                                    From mediaserver.song Left Outer Join (mediaserver.mediaitemmetadata natural join mediaserver.metadata natural join mediaserver.MetaDataType) On(song_id=media_id)
                                    Where lower(md_value) ~ lower(%s) And md_type_id = 1)
                    Group By song_id, song_title
                    Order By song_id;"""
            elif song_genre != '':
                sql = """
                    Select song_id, song_title, array_to_string(array_agg(distinct artist_name),',') as artists
                    From mediaserver.song Left Outer Join mediaserver.Song_Artists Using(song_id) Left Outer Join mediaserver.Artist On(performing_artist_id=artist_id)
                    Where lower(song_title) ~ lower(%s) And length < %s
                    And song_id in (Select song_id
                                    From mediaserver.song Left Outer Join (mediaserver.mediaitemmetadata natural join mediaserver.metadata natural join mediaserver.MetaDataType) On(song_id=media_id)
                                    Where lower(md_value) ~ lower(%s) And md_type_id = 1)
                    Group By song_id, song_title
                    Order By song_id;"""
            elif song_artist != '':
                sql = """
                    Select song_id, song_title, array_to_string(array_agg(distinct artist_name),',') as artists
                    From mediaserver.song Left Outer Join mediaserver.Song_Artists Using(song_id) Left Outer Join mediaserver.Artist On(performing_artist_id=artist_id)
                    Where lower(song_title) ~ lower(%s) And length < %s And lower(artist_name) ~ lower(%s)
                    Group By song_id, song_title
                    Order By song_id;"""
            else:
                sql = """
                    Select song_id, song_title, array_to_string(array_agg(distinct artist_name),',') as artists
                    From mediaserver.song Left Outer Join mediaserver.Song_Artists Using(song_id) Left Outer Join mediaserver.Artist On(performing_artist_id=artist_id)
                    Where lower(song_title) ~ lower(%s) And length < %s
                    Group By song_id, song_title
                    Order By song_id;"""
        if song_genre != '' and song_artist != '':
            r = dictfetchall(cur,sql,(song_title,song_length,song_artist,song_genre,))
        elif song_genre != '':
            r = dictfetchall(cur,sql,(song_title,song_length,song_genre,))
        elif song_artist != '':
            r = dictfetchall(cur,sql,(song_title,song_length,song_artist,))
        else:
            r = dictfetchall(cur,sql,(song_title,song_length,))
        print("return val is:")
        print(r)
        cur.close()                     # Close the cursor
        conn.close()                    # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting All Songs:", sys.exc_info()[0])
        raise
    cur.close()                     # Close the cursor
    conn.close()                    # Close the connection to the db
    return None

def tv_show_multi_term_search(tv_show_name, genre):
    conn = database_connect()
    if(conn is None):
        return None
    cur = conn.cursor()
    try:
        # Try executing the SQL and get from the database
        sql = """
            Select tvshow_id, tvshow_title, Count(episode)
            From mediaserver.TVShow left Outer Join mediaserver.TVEpisode using(tvshow_id)
            Where tvshow_id in(Select Distinct tvshow_id
            					From mediaserver.TVshow Left Outer Join (mediaserver.TVShowMetaData natural join mediaserver.metadata natural join mediaserver.MetaDataType) Using(tvshow_id)
            					Where lower(tvshow_title) ~ lower(%s) AND md_type_id = 2 AND lower(md_value) ~ lower(%s))
            Group By tvshow_id, tvshow_title
            Order By tvshow_id"""

        r = dictfetchall(cur,sql,(tv_show_name,genre,))
        print("return val is:")
        print(r)
        cur.close()                     # Close the cursor
        conn.close()                    # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting All TV Shows:", sys.exc_info()[0])
        raise
    cur.close()                     # Close the cursor
    conn.close()                    # Close the connection to the db
    return None

def podcast_multi_term_search(podcast_name, podcast_episode_count, podcast_episode_count_sign, podcast_genre):
    conn = database_connect()
    if(conn is None):
        return None
    cur = conn.cursor()
    try:
        # Try executing the SQL and get from the database
        if (podcast_episode_count_sign != '=' and podcast_episode_count_sign != '>' and podcast_episode_count_sign != '<'):
            return None

        if(podcast_episode_count.isnumeric() == False):
            return None

        if podcast_genre == '':
            if podcast_episode_count_sign == '=':
                sql = """
                    Select podcast_id, podcast_title, podcast_uri, podcast_last_updated, Count(media_id)
                    From mediaserver.Podcast Join mediaserver.PodcastEpisode Using(podcast_id)
                    Where podcast_id in (Select Distinct podcast_id
                                          From mediaserver.Podcast Left Outer Join (mediaserver.PodcastMetaData natural Join mediaserver.metadata natural join mediaserver.MetaDataType) Using(podcast_id)
                                          Where lower(podcast_title) ~ lower(%s))
                    Group By podcast_id, podcast_title, podcast_uri, podcast_last_updated
                    Having Count(media_id) = %s
                    Order By podcast_id;"""
            elif podcast_episode_count_sign == '>':
                sql = """
                    Select podcast_id, podcast_title, podcast_uri, podcast_last_updated, Count(media_id)
                    From mediaserver.Podcast Join mediaserver.PodcastEpisode Using(podcast_id)
                    Where podcast_id in (Select Distinct podcast_id
                                          From mediaserver.Podcast Left Outer Join (mediaserver.PodcastMetaData natural Join mediaserver.metadata natural join mediaserver.MetaDataType) Using(podcast_id)
                                          Where lower(podcast_title) ~ lower(%s))
                    Group By podcast_id, podcast_title, podcast_uri, podcast_last_updated
                    Having Count(media_id) > %s
                    Order By podcast_id;"""
            else:
                sql = """
                    Select podcast_id, podcast_title, podcast_uri, podcast_last_updated, Count(media_id)
                    From mediaserver.Podcast Join mediaserver.PodcastEpisode Using(podcast_id)
                    Where podcast_id in (Select Distinct podcast_id
                                          From mediaserver.Podcast Left Outer Join (mediaserver.PodcastMetaData natural Join mediaserver.metadata natural join mediaserver.MetaDataType) Using(podcast_id)
                                          Where lower(podcast_title) ~ lower(%s))
                    Group By podcast_id, podcast_title, podcast_uri, podcast_last_updated
                    Having Count(media_id) < %s
                    Order By podcast_id;"""
        else:
            if podcast_episode_count_sign == '=':
                sql = """
                    Select podcast_id, podcast_title, podcast_uri, podcast_last_updated, Count(media_id)
                    From mediaserver.Podcast Join mediaserver.PodcastEpisode Using(podcast_id)
                    Where podcast_id in (Select Distinct podcast_id
                                          From mediaserver.Podcast Left Outer Join (mediaserver.PodcastMetaData natural Join mediaserver.metadata natural join mediaserver.MetaDataType) Using(podcast_id)
                                          Where lower(podcast_title) ~ lower(%s) AND md_type_id = 6 AND lower(md_value) ~ lower(%s))
                    Group By podcast_id, podcast_title, podcast_uri, podcast_last_updated
                    Having Count(media_id) = %s
                    Order By podcast_id;"""
            elif podcast_episode_count_sign == '>':
                sql = """
                    Select podcast_id, podcast_title, podcast_uri, podcast_last_updated, Count(media_id)
                    From mediaserver.Podcast Join mediaserver.PodcastEpisode Using(podcast_id)
                    Where podcast_id in (Select Distinct podcast_id
                                          From mediaserver.Podcast Left Outer Join (mediaserver.PodcastMetaData natural Join mediaserver.metadata natural join mediaserver.MetaDataType) Using(podcast_id)
                                          Where lower(podcast_title) ~ lower(%s) AND md_type_id = 6 AND lower(md_value) ~ lower(%s))
                    Group By podcast_id, podcast_title, podcast_uri, podcast_last_updated
                    Having Count(media_id) > %s
                    Order By podcast_id;"""
            else:
                sql = """
                    Select podcast_id, podcast_title, podcast_uri, podcast_last_updated, Count(media_id)
                    From mediaserver.Podcast Join mediaserver.PodcastEpisode Using(podcast_id)
                    Where podcast_id in (Select Distinct podcast_id
                                          From mediaserver.Podcast Left Outer Join (mediaserver.PodcastMetaData natural Join mediaserver.metadata natural join mediaserver.MetaDataType) Using(podcast_id)
                                          Where lower(podcast_title) ~ lower(%s) AND md_type_id = 6 AND lower(md_value) ~ lower(%s))
                    Group By podcast_id, podcast_title, podcast_uri, podcast_last_updated
                    Having Count(media_id) < %s
                    Order By podcast_id;"""

        if podcast_genre != '':
            r = dictfetchall(cur,sql,(podcast_name,podcast_genre,podcast_episode_count,))
        else:
            r = dictfetchall(cur,sql,(podcast_name,podcast_episode_count,))

        print("return val is:")
        print(r)
        cur.close()                     # Close the cursor
        conn.close()                    # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting All Podcast:", sys.exc_info()[0])
        raise
    cur.close()                     # Close the cursor
    conn.close()                    # Close the connection to the db
    return None

def artist_multi_term_search(artist_name, artist_song_name):
    conn = database_connect()
    if(conn is None):
        return None
    cur = conn.cursor()
    try:
        # Try executing the SQL and get from the database
        if artist_song_name == '':
            sql = """
                Select artist_id, artist_name, Count(md_value)
                From mediaserver.artist Left Outer Join (mediaserver.ArtistMetaData Natural Join mediaserver.metadata natural join mediaserver.MetaDataType) Using(artist_id)
                Where artist_id in (Select artist_id
                					 From mediaserver.artist Left Outer Join (mediaserver.Song_Artists Natural Join mediaserver.Song) On(artist_id=performing_artist_id)
                					 Where lower(artist_name) ~ lower(%s))
                Group By artist_id, artist_name
                Order By artist_name;"""
        else:
            sql = """
                Select artist_id, artist_name, Count(md_value)
                From mediaserver.artist Left Outer Join (mediaserver.ArtistMetaData Natural Join mediaserver.metadata natural join mediaserver.MetaDataType) Using(artist_id)
                Where artist_id in (Select artist_id
                					 From mediaserver.artist Left Outer Join (mediaserver.Song_Artists Natural Join mediaserver.Song) On(artist_id=performing_artist_id)
                					 Where lower(artist_name) ~ lower(%s) And lower(song_title) ~ lower(%s))
                Group By artist_id, artist_name
                Order By artist_name;"""

        if artist_song_name == '':
            r = dictfetchall(cur,sql,(artist_name,))
        else:
            r = dictfetchall(cur,sql,(artist_name,artist_song_name,))
        print("return val is:")
        print(r)
        cur.close()                     # Close the cursor
        conn.close()                    # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting All Artists:", sys.exc_info()[0])
        raise
    cur.close()                     # Close the cursor
    conn.close()                    # Close the connection to the db
    return None

def album_multi_term_search(album_name, album_song_genre, album_artist_name):
    conn = database_connect()
    if(conn is None):
        return None
    cur = conn.cursor()
    try:
        # Try executing the SQL and get from the database
        if album_song_genre != '' and album_artist_name != '':
            sql = """
                Select album_id, album_title, Count(Distinct song_id), array_to_string(array_agg(distinct artist_name),',') as artists
                From mediaserver.Album Left Outer Join mediaserver.Album_Songs Using(album_id) Left Outer Join mediaserver.Song_Artists Using(song_id) Left Outer Join mediaserver.Artist On(performing_artist_id=artist_id)
                Where lower(album_title) ~ lower(%s)
                And album_id in (Select Distinct album_id
                			 	 From mediaserver.Album Left Outer Join mediaserver.Album_Songs Using(album_id) Left Outer Join mediaserver.Song_Artists Using(song_id) Left Outer Join mediaserver.Artist On(performing_artist_id=artist_id)
                			 	 Where lower(artist_name) ~ lower(%s))
                And album_id in (Select Distinct album_id
                				 From mediaserver.Album Left Outer Join mediaserver.Album_Songs Using(album_id) Left Outer Join (mediaserver.MediaItemMetaData Natural Join mediaserver.metadata Natural Join mediaserver.MetaDataType) On(song_id = media_id)
                				 Where lower(md_value) ~ lower(%s) AND md_type_id = 1)
                Group By album_id, album_title
                Order By album_id;"""
            r = dictfetchall(cur,sql,(album_name,album_artist_name,album_song_genre,))
        elif album_song_genre != '':
            sql = """
                Select album_id, album_title, Count(Distinct song_id), array_to_string(array_agg(distinct artist_name),',') as artists
                From mediaserver.Album Left Outer Join mediaserver.Album_Songs Using(album_id) Left Outer Join mediaserver.Song_Artists Using(song_id) Left Outer Join mediaserver.Artist On(performing_artist_id=artist_id)
                Where lower(album_title) ~ lower(%s)
                And album_id in (Select Distinct album_id
                				 From mediaserver.Album Left Outer Join mediaserver.Album_Songs Using(album_id) Left Outer Join (mediaserver.MediaItemMetaData Natural Join mediaserver.metadata Natural Join mediaserver.MetaDataType) On(song_id = media_id)
                				 Where lower(md_value) ~ lower(%s) AND md_type_id = 1)
                Group By album_id, album_title
                Order By album_id;"""
            r = dictfetchall(cur,sql,(album_name,album_song_genre,))
        elif album_artist_name != '':
            sql = """
                Select album_id, album_title, Count(Distinct song_id), array_to_string(array_agg(distinct artist_name),',') as artists
                From mediaserver.Album Left Outer Join mediaserver.Album_Songs Using(album_id) Left Outer Join mediaserver.Song_Artists Using(song_id) Left Outer Join mediaserver.Artist On(performing_artist_id=artist_id)
                Where lower(album_title) ~ lower(%s)
                And album_id in (Select Distinct album_id
                			 	 From mediaserver.Album Left Outer Join mediaserver.Album_Songs Using(album_id) Left Outer Join mediaserver.Song_Artists Using(song_id) Left Outer Join mediaserver.Artist On(performing_artist_id=artist_id)
                			 	 Where lower(artist_name) ~ lower(%s))
                Group By album_id, album_title
                Order By album_id;"""
            r = dictfetchall(cur,sql,(album_name,album_artist_name,))
        else:
            sql = """
                Select album_id, album_title, Count(Distinct song_id), array_to_string(array_agg(distinct artist_name),',') as artists
                From mediaserver.Album Left Outer Join mediaserver.Album_Songs Using(album_id) Left Outer Join mediaserver.Song_Artists Using(song_id) Left Outer Join mediaserver.Artist On(performing_artist_id=artist_id)
                Where lower(album_title) ~ lower(%s)
                Group By album_id, album_title
                Order By album_id;"""
            r = dictfetchall(cur,sql,(album_name,))

        print("return val is:")
        print(r)
        cur.close()                     # Close the cursor
        conn.close()                    # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting All Album:", sys.exc_info()[0])
        raise
    cur.close()                     # Close the cursor
    conn.close()                    # Close the connection to the db
    return None
