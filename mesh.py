import pygame
from vector3 import *

class Mesh:
    def __init__(self, name = "UnknownMesh"):
        self.name = name
        self.polygons = []

    def offset(self, v):
        new_polys = []
        for poly in self.polygons:
            new_poly = []
            for p in poly:
                new_poly.append(p + v)
            new_polys.append(new_poly)

        self.polygons = new_polys

    def render(self, screen, matrix, material):
        c = material.color.tuple3()        

        for poly in self.polygons:
            tpoly = []
            for v in poly:
                vout = v.to_np4()
                vout = vout @ matrix
                
                tpoly.append( ( screen.get_width() * 0.5 + vout[0] / vout[3], screen.get_height() * 0.5 - vout[1] / vout[3]) )

            pygame.draw.polygon(screen, c, tpoly, material.line_width)
    
    @staticmethod
    def create_pyramid(size, mesh = None):
        if (mesh == None):
            mesh = Mesh("UnknownPyramid")
            
        Mesh.create_triangle(vector3(size[0] * 0.5, 0, 0), vector3(0, 0, size[2] * 0.5), vector3(0, size[1] * 0.5, 0), mesh)
        Mesh.create_triangle(vector3(-size[0] * 0.5, 0, 0), vector3(0, 0, size[2] * 0.5), vector3(0, size[1] * 0.5, 0), mesh)
        Mesh.create_triangle(vector3(0, 0,  size[2] * 0.5), vector3(-size[0] * 0.5, 0), vector3(0, size[1] * 0.5, 0), mesh)
        Mesh.create_triangle(vector3(0, 0, -size[2] * 0.5), vector3( size[0] * 0.5, 0), vector3(0, size[1] * 0.5, 0), mesh)
       
        return mesh

    @staticmethod
    def create_triangle(origin, axis0, axis1, mesh):
        if (mesh == None):
            mesh = Mesh("UnknownTriangles")

        triangles = []

        triangles.append(origin - axis0 - axis1)
        triangles.append(origin - origin + axis1)
        triangles.append(origin + axis0 - axis1)
         
        mesh.polygons.append(triangles)

        return mesh
    
