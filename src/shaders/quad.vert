#version 330

in vec2 in_vert;     // corner in [0,1]
in vec2 in_offset;   // instance offset in grid coords

uniform ivec2 u_resolution; // grid cell counts
uniform vec2 u_screen; // screen size in pixels
uniform float u_padding; // inner padding inside each cell (0..1 fraction of cell)

void main() {
    // compute square cell size (in pixels) so grid preserves aspect ratio
    float cell_w = u_screen.x / float(u_resolution.x);
    float cell_h = u_screen.y / float(u_resolution.y);
    float cell = min(cell_w, cell_h);
    vec2 cell_px = vec2(cell, cell);

    // compute board size in pixels and top-left offset to center it
    vec2 board_px = cell_px * vec2(u_resolution);
    vec2 offset = (u_screen - board_px) * 0.5;

    // padding in pixels
    vec2 pad = cell_px * u_padding;

    // position in pixels (top-left origin)
    vec2 pos_px = offset + (in_offset + in_vert) * cell_px;

    // apply padding: shrink the quad toward its center by pad
    // in_vert in {0,1} - move corners inward/outward appropriately
    pos_px += (in_vert - 0.5) * ( -2.0 * pad );

    // to NDC
    vec2 ndc = (pos_px / u_screen) * 2.0 - 1.0;
    ndc.y = -ndc.y;
    gl_Position = vec4(ndc, 0.0, 1.0);
}