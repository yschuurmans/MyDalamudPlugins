# MyDalamudPlugins

## New central repository
To all those that used my plugin in the past, I have grouped my plugins together in a single repository. This means it is much easier for me to update the plugins, and much easier for you to find them, since you only need to add one repository to find all of my (currently 2) plugins! In order to install this new repository, follow the steps below in the Installation Guide.

&nbsp;
&nbsp;

## Warning!
I created these plugins for personal use. I never truly intended these as public plugins, so don't _**expect**_ any help or assistance if something doesn't work. But since quite a few people have since found their way to my plugins somehow, I figured I might as well write a readme.

## Installation guide
* **Be sure that "Enable in-game features" is on in the launcher settings to access in-game commands and features!**
* Access Dalamud's settings by typing `/xlsettings` in the chat window and pressing enter.
* Click on the "Experimental" tab.
* Copy and Paste in the following URL into one of the blank inputs under the "Custom Plugin Repositories" section: `https://raw.githubusercontent.com/yschuurmans/MyDalamudPlugins/master/pluginmaster.json`
* Click the "+" button to add it to the list.
* Check the "Enabled" box for your new entry.
* Click "Save and Close" at the bottom.
* Open Dalamud's plugin menu by typing `/xlplugins` in the chat window and pressing enter.
* Look for the "Money Tracker" plugin, and click on install.

## Migrating from the old XIVMoneyTracker
After you have installed the new repository, if you have previously used the XIVMoneyTracker repository, you have a couple more steps to go:
* Make sure to **remove** the line in your `/xlsettings` repository list that says:
`https://raw.githubusercontent.com/yschuurmans/FFXIVMoneyTracker/master/repo.json`
* After you do this, your plugin _may not automatically update_, to make sure it does:
* Open Dalamud's plugin menu by typing `/xlplugins` in the chat window and pressing enter.
* Look for the "Money Tracker" plugin, disable and uninstall version 4.*, and install version 5+
