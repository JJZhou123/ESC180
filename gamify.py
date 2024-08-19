def initialize():
    '''Initializes the global variables needed for the simulation.
    Note: this function is incomplete, and you may want to modify it'''

    global cur_hedons, cur_health

    global cur_time, star_time, cur_star_activity
    global last_activity, last_activity_duration
    global cont_time
    global bored_with_stars
    global star_amount
    global status
    global star_moment
    global total_time
    global prev_addhealth
    cur_hedons = 0
    cur_health = 0
    star_amount = 0
    status = "good"
    cur_star = None
    cur_star_activity = None
    cont_time = 0
    bored_with_stars = False
    star_moment = []
    last_activity = None
    last_activity_duration = 0
    star_time = 0
    cur_time = 0
    total_time = 0
    prev_addhealth = 0




def star_can_be_taken(activity):
    global star_time, cur_time, cur_star_activity, cont_time, bored_with_stars, last_activity, last_activity_duration

    if star_time == cur_time and bored_with_stars == False and cur_star_activity == activity:
        return True
    else:
        return False


def perform_activity(activity, duration):
    global cur_health, cur_hedons, last_activity, last_activity_duration, status, cur_star, cur_star_activity, cur_time, total_time, prev_addhealth
    if activity == "running":
        if cur_star_activity == "running" and cur_time == star_time and bored_with_stars == False:
            if duration <= 10:
                cur_hedons += 3*duration
            if duration > 10:
                cur_hedons += 30


        if last_activity == "running":
            last_activity_duration = last_activity_duration + duration
            cur_health -= prev_addhealth
            if last_activity_duration <= 180:
                cur_health += last_activity_duration*3
                cur_hedons -= duration*2
                prev_addhealth = last_activity_duration*3
            last_activity = "running"

            if last_activity_duration > 180:
                cur_health = cur_health + 540 + (last_activity_duration - 180)
                prev_addhealth = 540 + (last_activity_duration - 180)
                cur_hedons -= duration*2

            else:
                pass
            last_activity = "running"
            cur_time += duration


        if last_activity != "running":
            if status == "good":
                if duration <= 180:
                    cur_health += duration*3
                    prev_addhealth = duration*3
                if duration > 180:
                    cur_health += 540 + (duration - 180)
                    prev_addhealth = 540 + (duration - 180)
                if duration <= 10:
                    cur_hedons += duration*2
                if duration > 10:
                    cur_hedons = cur_hedons + 20 - ((duration - 10)*2)
                else:
                    pass

            if status == "tired":
                if duration <= 180:
                    cur_health += duration*3
                    cur_hedons -= duration*2
                    prev_addhealth = duration*3
                if duration > 180:
                    cur_health += 540 + (duration - 180)
                    prev_addhealth = 540 + (duration - 180)
                    cur_hedons -= duration*2
                else:
                    pass

            last_activity = "running"
            last_activity_duration = duration
            status = "tired"
            cur_time += duration





    if activity == "textbooks":
        if cur_star_activity == "textbooks" and cur_time == star_time and bored_with_stars == False:

            if duration <= 10:
                cur_hedons += 3*duration
            if duration > 10:
                cur_hedons += 30

        if status == "good":
            cur_health += duration*2
            if duration <= 20:
                cur_hedons += duration
            if duration > 20:
                cur_hedons = cur_hedons + 20 - (duration - 20)
            else:
                pass

        if status == "tired":
            cur_health += duration*2
            cur_hedons -= duration*2
            last_activity = "textbooks"
            last_activity_duration = duration

        status = "tired"
        last_activity = "textbooks"
        last_activity_duration = duration
        cur_time += duration



    if activity == "resting":
        if last_activity == "resting":
            last_activity_duration = last_activity_duration + duration
            last_activity = "resting"
            cur_time += duration
            if last_activity_duration >= 120:
                status = "good"


        if last_activity != "resting":
            if duration >= 120:
                status = "good"
                last_activity_duration = duration
                last_activity = "resting"
                cur_time += duration
            if duration < 120:
                last_activity = "resting"
                last_activity_duration = duration
                cur_time += duration


    else:
        pass

    #print(cur_health,cur_hedons)
    #print(status)

def get_cur_hedons():
    global cur_hedons
    return cur_hedons

def get_cur_health():
    global cur_health
    return cur_health

def offer_star(activity):
    global star_time, cur_star_activity, cur_time, cont_time, star_amount, star_moment, bored_with_stars
    star_time = cur_time
    cur_star_activity = activity
    star_amount += 1      # star_amount: how many times of offer_star has appeared
    if star_amount < 3:   # star_moment: a list of time where offer_star has appeared
        star_moment.append(star_time)
        #print(star_moment)
    if star_amount >= 3:
        star_moment.append(star_time)
        cont_time = star_moment[2] - star_moment[0]
        if cont_time <= 120:
            bored_with_stars = True

        else:
            star_moment.pop(0)

   # print(star_moment)




def most_fun_activity_minute():
    global cur_star_activity, cur_time, star_time, bored_with_stars
    if status == "good":
        if cur_star_activity == "running" and cur_time == star_time and bored_with_stars == False:
            return "running"

        if cur_star_activity == "textbooks" and cur_time == star_time and bored_with_stars == False:
            return "textbooks"
        else:
            return "running"

    if status == "tired":
        if cur_star_activity == "running" and cur_time == star_time and bored_with_stars == False:
            return "running"

        if cur_star_activity == "textbooks" and cur_time == star_time and bored_with_stars == False:
            return "textbooks"
        else:
            return "resting"

################################################################################
#These functions are not required, but we recommend that you use them anyway
#as helper functions

def get_effective_minutes_left_hedons(activity):
    '''Return the number of minutes during which the user will get the full
    amount of hedons for activity activity'''
    pass

def get_effective_minutes_left_health(activity):
    pass

def estimate_hedons_delta(activity, duration):
    '''Return the amount of hedons the user would get for performing activity
    activity for duration minutes'''
    pass


def estimate_health_delta(activity, duration):
    pass

################################################################################




if __name__ == '__main__':
    initialize()
    perform_activity("running", 30)
    print(get_cur_hedons())            #-20 = 10 * 2 + 20 * (-2)
    print(get_cur_health())            #90 = 30 * 3
    print(most_fun_activity_minute())  #resting
    perform_activity("resting", 30)
    offer_star("running")
    print(cur_health, cur_hedons)   ###
    print(most_fun_activity_minute())  #running
    perform_activity("textbooks", 30)
    print(cur_health, cur_hedons)   ###
    print(get_cur_health())            #150 = 90 + 30*2
    print(get_cur_hedons())            #-80 = -20 + 30 * (-2)
    offer_star("running")
    perform_activity("running", 20)
    print(cur_health, cur_hedons)   ###
    print(get_cur_health())            #210 = 150 + 20 * 3
    print(get_cur_hedons())            #-90 = -80 + 10 * (3-2) + 10 * (-2)
    print(last_activity, last_activity_duration)
    perform_activity("running", 170)
    print(cur_health, cur_hedons)   ###
    print(get_cur_health())            #700 = 210 + 160 * 3 + 10
    print(get_cur_hedons())            #-430 = -90 + 170 * (-2)



