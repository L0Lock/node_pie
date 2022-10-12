import bpy
from bpy.types import UILayout
from bpy.props import BoolProperty, FloatProperty
from .npie_helpers import get_prefs
from .npie_ui import NPIE_MT_node_pie, draw_section, draw_inline_prop


class NodePiePrefs(bpy.types.AddonPreferences):
    """Node pie"""

    bl_idname: str = __package__.split(".")[0]

    layout: UILayout
    node_pie_enabled: BoolProperty(name="Enable node pie", default=True)

    npie_variable_sizes: BoolProperty(
        name="Use variable size",
        default=True,
        description="Whether to increase the size of node buttons that are used most often",
    )

    npie_normal_size: FloatProperty(
        name="Normal size",
        default=1,
        description="The default size of the nodes buttons",
    )

    npie_max_size: FloatProperty(
        name="Max size",
        default=2.5,
        description="The size of the most popular nodes",
    )

    npie_show_node_groups: BoolProperty(
        name="Show node groups",
        default=True,
        description="Whether to show node groups in the pie menu or not",
    )

    npie_color_size: FloatProperty(
        name="Color bar size",
        default=.02,
        description="Having this value too low can cause the colors to disapear.",
        subtype="FACTOR",
        min=0,
        max=1,
    )

    npie_freeze_popularity: BoolProperty(
        name="Freeze popularity",
        default=False,
        description="Prevent new changes the popularity of nodes.",
    )

    def draw(self, context):
        layout = self.layout
        # layout = draw_enabled_button(layout, self, "node_pie_enabled")
        prefs = get_prefs(context)
        layout = layout.grid_flow(row_major=True, even_columns=True)

        fac = .515
        col = draw_section(layout, "Node Popularity")
        draw_inline_prop(col, prefs, "npie_variable_sizes", factor=fac)
        draw_inline_prop(col, prefs, "npie_normal_size", factor=fac)
        draw_inline_prop(col, prefs, "npie_max_size", factor=fac)
        row = col.row(align=True)
        row.scale_y = 1.5
        row.prop(prefs, "npie_freeze_popularity", text="Freeze popularity", icon="FREEZE", toggle=True)
        row.operator("node_pie.reset_popularity", icon="FILE_REFRESH")

        col = draw_section(layout, "General")
        draw_inline_prop(col, prefs, "npie_show_node_groups", factor=fac)
        draw_inline_prop(col, prefs, "npie_color_size", factor=fac)

        col = draw_section(layout, "Keymap")
        global addon_keymaps
        for km, kmi in addon_keymaps:
            row = col.row(align=True)
            row.active = kmi.active
            sub = row.row(align=True)
            sub.prop(kmi, "active", text="")
            sub = row.row(align=True)
            sub.scale_x = .5
            sub.prop(kmi, "type", full_event=True, text="")
            sub = row.row(align=True)
            sub.enabled = True
            sub.operator("preferences.keyitem_restore", text="", icon="X").item_id = kmi.id


addon_keymaps = []


def register():
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name='Node Editor', space_type='NODE_EDITOR')

        kmi = km.keymap_items.new(
            "wm.call_menu_pie",
            type='LEFTMOUSE',
            value='PRESS',
            ctrl=True,
        )
        kmi.properties.name = NPIE_MT_node_pie.__name__
        addon_keymaps.append((km, kmi))
        kmi = km.keymap_items.new(
            "wm.call_menu_pie",
            type='A',
            value='PRESS',
            ctrl=True,
        )
        kmi.properties.name = NPIE_MT_node_pie.__name__
        # addon_keymaps.append((km, kmi))
        # kmi = km.keymap_items.new(
        #     "wm.call_menu_pie",
        #     type='RIGHTMOUSE',
        #     value='CLICK_DRAG',
        # )
        # kmi.properties.name = NPIE_MT_node_pie.__name__
        # addon_keymaps.append((km, kmi))


def unregister():
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()
