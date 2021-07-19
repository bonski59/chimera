import tkinter as tk


def help_window():
    newwindow = tk.Toplevel()
    newwindow.columnconfigure([0, 1, 2], minsize=40)
    newwindow.rowconfigure([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15], minsize=0)
    helplabel = tk.Label(newwindow,
                         text="User Manual",
                         width=12,
                         height=7
                         )
    helplabel.grid(row=1, column=1)
    initializetext = tk.Label(newwindow,
                              text="First, click the Initialize button in the top center of the GUI. This will search "
                                   "for all online DREDs.  \n "
                                   "Next, select the DRED you wish to output audio to using the 'select DRED' "
                                   "dropdown menu. If the DRED you wish to use does not appear, it is offline. \n "
                                   "Next, select the frequency you wish the sound to play at from the 'select "
                                   "frequency' dropdown OR enter a custom frequnecy in the 'custom frequency' box. \n "
                                   "Next, select the sound you wish to play from the 'select sound' dropdown OR enter "
                                   "a custom sound in the 'custom sound' box. \n "
                                   "Lastly, select 'play sound' and the sound will play on the selected DRED",
                              width=120,
                              height=5
                              )
    initializetext.grid(row=2, column=1)
    queuetext = tk.Label(newwindow,
                         text="You also have the option to create a queue of multiple sounds to play. \n"
                              "Simply initialize, select frequency and sound, then select the 'add to queue' option. \n"
                              "Once your queue is complete, select 'play entire queue'. All selected sounds will play "
                              "at their set frequecies in the order specified. \n "
                              "NOTE: You can not add a queue to CRON as this is not supported by CRON jobs",
                         width=120,
                         height=5
                         )
    queuetext.grid(row=3, column=1)
    crontext = tk.Label(newwindow,
                        text="If you wish to set a cronjob to play at a set time you can schedule a 'cronjob' \n"
                             "Select DRED, frequency, and sound, then fill out the desired minutes, hours, "
                             "day of month, month, and day of week. \n "
                             "You can use a wildcard (*) to select every available value. Or you can enter a number "
                             "value. You can also use the */ option to play the sound every set interval. \n "
                             "You can not use an numbers before '/', only wildcards. EX. '13/30' is not a valid "
                             "command.\n "
                             "All operators are '*' (any value) ',' (list values) '-' (value range) '/' (step "
                             "values). Number values also start from 0. \n "
                             "Ex: If you want to play a sound every 5 minutes at 1600 - 1800 5 days a week the syntax "
                             "will be '*/5 16-18 * * 0,1,2,3,4' \n "
                             "You also have the option to queue the same sound to play multiple times by using ';' to "
                             "add multiple cron jobs at once. \n "
                             " You can not add multiple sound files at once.\n \n"
                             "You can view all cronjobs by selecting 'show CRON jobs'. You can reset all cron jobs by "
                             "selecting 'reset CRON jobs', \n "
                             "or you can remove a specific job by entering the job code in 'remove CRON job' (without "
                             "the # sign) \n",
                        width=120,
                        height=12
                        )
    crontext.grid(row=4, column=1)
