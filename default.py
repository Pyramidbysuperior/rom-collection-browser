# Copyright (C) 2010 Malte Loepmann (maloep@googlemail.com)
#
# This program is free software; you can redistribute it and/or modify it under the terms 
# of the GNU General Public License as published by the Free Software Foundation; 
# either version 2 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; 
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program; 
# if not, see <http://www.gnu.org/licenses/>.

# I have built this script from scratch but you sure will find some lines or ideas that are taken 
# from other xbmc scripts. Some basic ideas are taken from Redsandros "Arcade Browser" and I often 
# had a look at Nuka1195's "Apple Movie Trailers" script while implementing this one. Thanks for your work!



import os
import sys

# Shared resources
BASE_RESOURCE_PATH = os.path.join( os.getcwd(), "resources" )
sys.path.append( os.path.join( BASE_RESOURCE_PATH, "lib" ) )
# append the proper platforms folder to our path, xbox is the same as win32
env = ( os.environ.get( "OS", "win32" ), "win32", )[ os.environ.get( "OS", "win32" ) == "xbox" ]
sys.path.append( os.path.join( BASE_RESOURCE_PATH, "platform_libraries", env ) )

#import xbmc
# create our language object
#__language__ = xbmc.Language( os.getcwd() ).getLocalizedString

# Start the main gui
if __name__ == "__main__":
    # only run if compatible
    #if ( _check_compatible() ):
        # main window
        import gui