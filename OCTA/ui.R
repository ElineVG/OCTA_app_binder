ui <- function(input, output, session) {miniPage(
  tags$head(
    tags$style(HTML(".bucket-list-container {min-height: 500px;}")),
    tags$script(
      "$( function() {
      $( '.delete_dropped' ).droppable({
      drop: function(e, ui) {
      $(ui.helper).remove();
      }
      })
      });

      $( function() {
      $( '.cloned' ).draggable({
      helper: 'clone',
      connectToSortable: '#shapedest',
      drop: function(e, ui) {
      $(ui.helper).remove();
      }
      })
      });      
      
      $( function() {
      $( '.cloned2' ).draggable({
      helper: 'clone',
      connectToSortable: '#colordest',
      drop: function(e, ui) {
      $(ui.helper).remove();
      }
      })
      });"
    )
  ),
  setBackgroundColor(color = '#F8F8F8'),
  miniTitleBar("OCTA toolbox"),
  miniTabstripPanel(
    miniTabPanel("Stimulus", icon = icon("image"),
                 miniContentPanel(
                   htmlOutput("svgplot")
                 )
    ),
    miniTabPanel("Code", icon = icon("code"),
                 miniContentPanel(
                   fillRow(flex = c(4,6),
                     htmlOutput("svgplot2"),
                     fillCol(flex = c(2,16),
                       fluidRow(
                         downloadButton("downloadsvg", "Download .svg"),
                         downloadButton("downloadjson", "Download .json"),
                         downloadButton("downloadtxt", "Download elements .txt"),
                         downloadButton("downloadtxtparams", "Download params .txt")),
                         textOutput("svgprint")
                     )
                   )
                 )
    ),
    miniTabPanel("Shapes", icon = icon("shapes"),
                 miniContentPanel(
                   
                   
                   fillRow(flex = c(4,6),
                           htmlOutput("svgplot3"),
                           fillCol(flex = c(2,2,8),
                                   fillRow(selectInput("shapepattern", "Shape pattern:", selected = 'identity',
                                               c("iterative" = "identity", "symmetric", "repetitive" = "repeateach", "random")),
                                   
                                   selectInput("shapedim", "Shape axis:", selected = 'row',
                                               c("row" = "col", "column" = "row", "right diagonal" = "rightdiag", "left diagonal" = "leftdiag"))),
                                   
                                   column(12, 
                                          h4("Available shapes"),
                                          jqui_sortable(div(id = "shapesource", class="delete_dropped",
                                                            lapply(allshapes, shapeblocks, data = allshapes),
                                                            style = "padding:10px;min-height:50px;"),
                                                        options = list(connectWith = "#shapedest"))),
                                   column(12, h4("Shapes to use"),
                                          jqui_sortable(div(id = "shapedest", 
                                                            lapply(SHAPE, shapeblocks2, data = SHAPE), style = "padding:10px;min-height:50px")
                                          ))

                                   # bucket_list(
                                   #   header = "",
                                   #   group_name = "bucket_list_group",
                                   #   orientation = "horizontal",
                                   #   add_rank_list(
                                   #     text = "Available shapes",
                                   #     labels = NOSHAPE,
                                   #     input_id = "noshape"
                                   #   ),
                                   #   add_rank_list(
                                   #     text = "Shapes to be used",
                                   #     labels = SHAPE,
                                   #     input_id = "shape"
                                   #   ))
                           )
                   ))
                 
    ),
    miniTabPanel("Colors", icon = icon("palette"),
                 miniContentPanel(
      
                           fillRow(flex = c(4,6),
                             htmlOutput("svgplot4"),
                             fillCol(flex = c(2,3,8),
                               fillRow(selectInput("colorpattern", "Color pattern:", selected = sample(c("identity", "symmetric", "repeateach", "random"), size = 1),
                                                   c("iterative" = "identity", "gradient", "symmetric", "repetitive" = "repeateach", "random")),
                                       selectInput("colordim", "Color axis:", selected = sample(c("col", "row", "rightdiag", "leftdiag"), size = 1),
                                                   c("row" = "col", "column" = "row", "right diagonal" = "rightdiag", "left diagonal" = "leftdiag"))),
                               column(12, 
                                      h4("Available colors"),
                                      jqui_sortable(div(id = "colorsource", class="delete_dropped",
                                                        lapply(allcolors, colorblocks, data = allcolors),
                                                        style = "padding:10px;min-height:50px;"),
                                                    options = list(connectWith = "#colordest"))),
                               column(12, h4("Colors to use"),
                                      jqui_sortable(div(id = "colordest", 
                                                        lapply(COLOR, colorblocks2, data = COLOR), style = "padding:10px;min-height:50px")
                                      ))
                               # bucket_list(
                               # header = "",
                               # group_name = "bucket_list_group2",
                               # orientation = "horizontal",
                               # add_rank_list(
                               #   text = "Available colors",
                               #   labels = NOCOLOR,
                               #   input_id = "nocolor"
                               # ),
                               # add_rank_list(
                               #   text = "Colors to be used",
                               #   labels = COLOR,
                               #   input_id = "color"
                               # ))
                             )
                           )
                   
                 )
                 
    ),
    miniTabPanel("Orientations", icon = icon("location-arrow"),
                 miniContentPanel(
                   
                   fillRow(flex = c(4,6),
                           htmlOutput("svgplot7"),
                           fillCol(flex = c(2,8),
                                   fillRow(
                                     selectInput("orientationpattern", "Orientation pattern:", selected = sample(c("identity", "symmetric", "repeateach", "random"), size = 1),
                                                 c("iterative" = "identity", "symmetric", "repetitive" = "repeateach", "random")),
                                     selectInput("orientationdim", "Orientation axis:", selected = sample(c("col", "row", "rightdiag", "leftdiag"), size = 1),
                                                 c("row" = "col", "column" = "row", "right diagonal" = "rightdiag", "left diagonal" = "leftdiag"))),
                                   
                                   checkboxGroupInput("orientation", "Orientation:", selected = sample(c(15,25,35), size = 1), inline = T,
                                                      c("small" = 15,
                                                        "medium" = 25,
                                                        "large" = 35))
                           )
                   )
                 )
                 
                 
    ),
    miniTabPanel("Parameters", icon = icon("sliders"),
                 miniContentPanel(
                  
                   fillRow(flex = c(4,6),
                     htmlOutput("svgplot5"),
                     fillCol(flex = c(3,3,3,3,3),
                       
                        fillRow(
                             numericInput("nrows", "Number of rows:", NROW,
                                          min = 5, max = 9),
                             numericInput("ncols", "Number of columns:", NROW,
                                          min = 5, max = 9)
                        ),
                        fillRow(
                             numericInput("xdist", "X distance:", NDIST,
                                          min = 20, max = 40),
                             numericInput("ydist", "Y distance:", NDIST,
                                          min = 20, max = 40)
                        ),
                        fillRow(
                             numericInput("startx", "Start x:", 60,
                                          min = 30, max = 60),
                             numericInput("starty", "Start y:", 60,
                                          min = 30, max = 60)
                        ),
                        fillRow(
                          numericInput("jitterscale", "jitterscale:", 0,
                                       min = 0, max = 5)
                        ),
                        fillRow(
                             checkboxGroupInput("size", "Size:", selected = sample(c(15, 20, 25), size = sample(c(1:3), size = 1)), inline = T,
                                                c("small" = 15,
                                                  "medium" = 20,
                                                  "large" = 25)),
                             checkboxGroupInput("shapexyratio", "Shape xyratio:", selected = 1, inline = T,
                                                c("small" = 0.5,
                                                  "medium" = 1,
                                                  "large" = 2))
                        )

                   )
                   )

                  )
                 
    ),
    

    
    miniTabPanel("Table", icon = icon("table"),
                 miniContentPanel(
                   #fillRow(
                   #rHandsontableOutput("parametershot"), height = "10%"),
                   fillRow(flex = c(4,6),
                   htmlOutput("svgplot6", height = "100%"), 
                   rHandsontableOutput("hot")
                   )
                 )
                 
    )
  )
)}
