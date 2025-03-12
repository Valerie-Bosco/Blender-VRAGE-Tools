# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name" : "Vrage Tools",
    "author" : "Keen Software House",
    "description" : "",
    "blender" : (4, 0, 0),
    "version" : (0, 1, 2),
    "location" : "",
    "warning" : "",
    "category" : "Generic"
}


import bpy
from .utilities import auto_load
from . import global_variables

from .scene.scene               import scene_register, scene_unregister
from .view_layer.view_layer     import view_layer_register, view_layer_unregister


auto_load.init()


def register():
    global_variables.create()
    auto_load.register()

    scene_register()
    view_layer_register()


def unregister():
    global_variables.destroy()
    auto_load.unregister()

    scene_unregister()
    view_layer_unregister()