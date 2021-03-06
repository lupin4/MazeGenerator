import bpy
from random import seed, random
from . modifier_manager import add_driver_to
from .. visual . cell_visual import DISTANCE, UNIFORM
# from .. visual . maze_visual import MazeVisual


class MaterialManager:
    def __init__(self, maze_visual):
        self.mv = maze_visual
        self.cell_rgb_node = None
        self.cell_vertex_colors_node = None
        self.cell_sep_rgb_node = None
        self.cell_value_node = None
        self.cell_math_node = None
        self.cell_math_alpha_node = None
        self.cell_cr_distance_node = None
        self.cell_mix_longest_distance_node = None
        self.cell_mix_under_node = None
        self.cell_hsv_node = None
        self.cell_bsdf_node = None
        self.cell_output_node = None

    def update(self, maze_visual):
        self.mv = maze_visual

    def init_cell_rgb_node(self, nodes, props):
        try:
            self.cell_rgb_node = nodes['cell_rgb_node']
        except KeyError:
            self.cell_rgb_node = nodes.new(type='ShaderNodeRGB')
            self.cell_rgb_node.name = 'cell_rgb_node'
        finally:
            seed(props.seed_color)
            self.cell_rgb_node.outputs['Color'].default_value = (random(), random(), random(), 1)
            self.cell_rgb_node.location = -400, -300

    def init_cell_vertex_colors_node(self, nodes, props):
        try:
            self.cell_vertex_colors_node = nodes['cell_vertex_colors_node']
        except KeyError:
            self.cell_vertex_colors_node = nodes.new(type='ShaderNodeVertexColor')
            self.cell_vertex_colors_node.name = 'cell_vertex_colors_node'
        finally:
            self.cell_vertex_colors_node.layer_name = props.paint_style
            self.cell_vertex_colors_node.location = -1200, 0

    def init_cell_hsv_node(self, nodes, scene):
        try:
            self.cell_hsv_node = nodes['cell_hsv_node']
        except KeyError:
            self.cell_hsv_node = nodes.new(type='ShaderNodeHueSaturation')
            self.cell_hsv_node.name = 'cell_hsv_node'
        finally:
            self.cell_hsv_node.location = -200, 0
            if scene:
                add_driver_to(self.cell_hsv_node.inputs['Hue'], 'default_value', 'hue_shift', 'SCENE', scene, 'mg_props.hue_shift', '0.5 + hue_shift')
                add_driver_to(self.cell_hsv_node.inputs['Saturation'], 'default_value', 'sat_shift', 'SCENE', scene, 'mg_props.saturation_shift', '1 + sat_shift')
                add_driver_to(self.cell_hsv_node.inputs['Value'], 'default_value', 'val_shift', 'SCENE', scene, 'mg_props.value_shift', '1 + val_shift')

    def init_cell_bsdf_node(self, nodes):
        try:
            self.cell_bsdf_node = nodes['cell_bsdf_node']
        except KeyError:
            self.cell_bsdf_node = nodes.new(type='ShaderNodeBsdfPrincipled')
            self.cell_bsdf_node.name = 'cell_bsdf_node'

    def init_cell_sep_rgb_node(self, nodes):
        try:
            self.cell_sep_rgb_node = nodes['cell_sep_rgb_node']
        except KeyError:
            self.cell_sep_rgb_node = nodes.new(type='ShaderNodeSeparateRGB')
            self.cell_sep_rgb_node.name = 'cell_sep_rgb_node'
        finally:
            self.cell_sep_rgb_node.location = -1000, 0

    def init_cell_mix_distance_node(self, nodes, props):
        try:
            self.cell_cr_distance_node = nodes['cell_cr_distance_node']
        except KeyError:
            self.cell_cr_distance_node = nodes.new(type='ShaderNodeValToRGB')
            self.cell_cr_distance_node.name = 'cell_cr_distance_node'
            self.cell_cr_distance_node.color_ramp.elements[0].color = (0, 1, 0, 1)
            self.cell_cr_distance_node.color_ramp.elements[1].color = [1, 0, 0, 1]
        finally:
            self.cell_cr_distance_node.location = -800, -100

    def init_cell_math_node(self, nodes, props):
        try:
            self.cell_math_node = nodes['cell_math_node']
        except KeyError:
            self.cell_math_node = nodes.new(type='ShaderNodeMath')
            self.cell_math_node.name = 'cell_math_node'
        finally:
            self.cell_math_node.operation = 'MULTIPLY'
            self.cell_math_node.inputs[1].default_value = props.show_only_longest_path
            self.cell_math_node.location = -800, 100

    def init_cell_math_alpha_node(self, nodes):
        try:
            self.cell_math_alpha_node = nodes['cell_math_alpha_node']
        except KeyError:
            self.cell_math_alpha_node = nodes.new(type='ShaderNodeMath')
            self.cell_math_alpha_node.name = 'cell_math_alpha_node'
        finally:
            self.cell_math_alpha_node.operation = 'ADD'
            self.cell_math_alpha_node.location = -800, 300

    def init_cell_value_node(self, nodes):
        try:
            self.cell_value_node = nodes['cell_value_node']
        except KeyError:
            self.cell_value_node = nodes.new(type='ShaderNodeValue')
            self.cell_value_node.name = 'cell_value_node'
        finally:
            self.cell_value_node.location = -1000, -400

    def init_cell_mix_under_node(self, nodes):
        try:
            self.cell_mix_under_node = nodes['cell_mix_under_node']
        except KeyError:
            self.cell_mix_under_node = nodes.new(type='ShaderNodeMixRGB')
            self.cell_mix_under_node.name = 'cell_mix_under_node'
        finally:
            self.cell_mix_under_node.blend_type = 'SUBTRACT'
            self.cell_mix_under_node.inputs[0].default_value = 0.5
            self.cell_mix_under_node.location = -800, -400

    def init_cell_mix_longest_distance_node(self, nodes):
        try:
            self.cell_mix_longest_distance_node = nodes['cell_mix_longest_distance_node']
        except KeyError:
            self.cell_mix_longest_distance_node = nodes.new(type='ShaderNodeMixRGB')
            self.cell_mix_longest_distance_node.name = 'cell_mix_longest_distance_node'
        finally:
            self.cell_mix_longest_distance_node.inputs[2].default_value = [0.5, 0.5, 0.5, 1]
            self.cell_mix_longest_distance_node.location = -400, 0

    def init_cell_output_node(self, nodes):
        try:
            self.cell_output_node = nodes['cell_output_node']
        except KeyError:
            self.cell_output_node = nodes.new(type='ShaderNodeOutputMaterial')
            self.cell_output_node.name = 'cell_output_node'
        finally:
            self.cell_output_node.location = 300, 0

    def set_materials(self):
        self.set_cell_material()
        self.set_cell_contour_material()
        self.set_wall_material()

    def set_cell_material(self):
        already_created = False
        obj_cells = self.mv.obj_cells
        props = self.mv.props
        scene = self.mv.scene

        try:
            mat = obj_cells.material_slots[0].material
            already_created = True
        except IndexError:
            mat = bpy.data.materials.new("mat_cells")
            obj_cells.data.materials.append(mat)
        mat.use_nodes = True

        nodes = mat.node_tree.nodes
        if not already_created or props.auto_overwrite:
            nodes.clear()

        self.init_cell_rgb_node(nodes, props)
        self.init_cell_vertex_colors_node(nodes, props)
        self.init_cell_hsv_node(nodes, scene)
        self.init_cell_sep_rgb_node(nodes)
        self.init_cell_mix_distance_node(nodes, props)
        self.init_cell_math_node(nodes, props)
        self.init_cell_math_alpha_node(nodes)
        self.init_cell_value_node(nodes)
        self.init_cell_mix_under_node(nodes)
        self.init_cell_mix_longest_distance_node(nodes)
        self.init_cell_bsdf_node(nodes)
        self.init_cell_output_node(nodes)

        try:
            self.cell_vertex_colors_node.layer_name = props.paint_style
            links = mat.node_tree.links
            if props.paint_style == DISTANCE:
                links.new(self.cell_vertex_colors_node.outputs[0], self.cell_sep_rgb_node.inputs[0])
                links.new(self.cell_sep_rgb_node.outputs[0], self.cell_cr_distance_node.inputs[0])
                links.new(self.cell_sep_rgb_node.outputs[1], self.cell_math_node.inputs[0])
                links.new(self.cell_value_node.outputs[0], self.cell_mix_under_node.inputs[1])
                links.new(self.cell_sep_rgb_node.outputs[2], self.cell_mix_under_node.inputs[2])
                links.new(self.cell_mix_under_node.outputs[0], self.cell_hsv_node.inputs[2])

                links.new(self.cell_math_node.outputs[0], self.cell_math_alpha_node.inputs[0])
                links.new(self.cell_vertex_colors_node.outputs[1], self.cell_math_alpha_node.inputs[1])
                links.new(self.cell_math_alpha_node.outputs[0], self.cell_mix_longest_distance_node.inputs[0])

                links.new(self.cell_cr_distance_node.outputs[0], self.cell_mix_longest_distance_node.inputs[1])
                links.new(self.cell_mix_longest_distance_node.outputs[0], self.cell_hsv_node.inputs[4])

                add_driver_to(self.cell_value_node.outputs[0], 'default_value', 'val_shift', 'SCENE', scene, 'mg_props.value_shift', '1 + val_shift')
                add_driver_to(self.cell_mix_under_node.inputs[0], 'default_value', 'val_shift', 'SCENE', scene, 'mg_props.value_shift', '(val_shift + 1)/2')
            elif props.paint_style == UNIFORM:
                links.new(self.cell_rgb_node.outputs[0], self.cell_hsv_node.inputs[4])
            else:
                links.new(self.cell_vertex_colors_node.outputs[0], self.cell_hsv_node.inputs[4])

            links.new(self.cell_hsv_node.outputs[0], self.cell_bsdf_node.inputs[0])
            links.new(self.cell_bsdf_node.outputs[0], self.cell_output_node.inputs[0])

        except IndexError:
            pass
        except AttributeError:
            pass

    def set_cell_contour_material(self):
        props = self.mv.props
        obj_cells = self.mv.obj_cells
        try:
            mat = obj_cells.material_slots[1].material
            if not props.auto_overwrite:
                return
        except IndexError:
            mat = bpy.data.materials.new("mat_cells_contour")
            obj_cells.data.materials.append(mat)
        mat.use_nodes = True

        mat.node_tree.nodes['Principled BSDF'].inputs[0].default_value = (0, 0, 0, 1)
        mat.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value = 1

    def set_wall_material(self):
        props = self.mv.props
        obj_walls = self.mv.obj_walls
        try:
            mat = obj_walls.material_slots[0].material
            if not props.auto_overwrite:
                return
        except IndexError:
            mat = bpy.data.materials.new("mat_walls")
            obj_walls.data.materials.append(mat)
        mat.use_nodes = True

        nodes = mat.node_tree.nodes
        nodes.clear()

        vertex_colors = nodes.new(type='ShaderNodeRGB')
        vertex_colors.location = -400, 0
        color = props.wall_color
        vertex_colors.outputs['Color'].default_value = [color[0], color[1], color[2], 1]

        principled = nodes.new(type='ShaderNodeBsdfPrincipled')

        output = nodes.new(type='ShaderNodeOutputMaterial')
        output.location = 300, 0

        links = mat.node_tree.links
        links.new(vertex_colors.outputs[0], principled.inputs[0])
        links.new(principled.outputs[0], output.inputs[0])
