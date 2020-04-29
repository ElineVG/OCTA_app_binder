library(tidyverse)
library(jsonlite)
library(shiny)
library(rhandsontable)
library(reticulate)
library(htmltools)
library(miniUI)
library(shinyjs)
library(shinyjqui)
library(shinyWidgets)

reticulate::source_python('OCTA_functions_inline_28_03_2020.py')

allcolors <- c(
  "#0000FF" = "blue",
  "#FF0000" = "red",
  "#00FF00" = "green",
  "#FF7000" = "orange",
  "#FFFF00" = "yellow",
  "#80FF00" = "chartreuse",
  "#00FF80" = "springgreen",
  "#00FFFF" = "aqua",
  "#0080FF" = "dodgerblue",
  "#7F00FF" = "indigo",
  "#FF00FF" = "magenta",
  "#FF007F" = "deeppink"
)

NROW <- sample(c(4:8), size = 1)
NDIST <- sample(c(30:40), size = 1)

# allcolors <- c(
#   "blue",
#   "red",
#   "green",
#   "orange",
#   "yellow",
#   "chartreuse",
#   "springgreen",
#   "aqua",
#   "dodgerblue",
#   "indigo",
#   "magenta",
#   "deeppink"
# )

# allcolors <- c(
#   "#9C4B9C" = "purple",
#   "#5EA1D8" = "blue",
#   "#54C4D0" = "cyan",
#   "#62BD80" = "green",
#   "#B2D135" = "chartreuse",
#   "#FCE533" = "yellow",
#   "#F39130" = "orange",
#   "#ED4959" = "red"
# )

# #own approximation Palmer & Schloss
# allcolors <- c(
#   "#9472DE",
#   "#00B2F8",
#   "#3ED1DA",
#   "#47C294",
#   "#CBE46D",
#   "#FFF870",
#   "#FFAE57",
#   "#E1685D"
# )

# #colors Astrid
# allcolors <- c(
#   "#9C4B9C",
#   "#5EA1D8",
#   "#54C4D0",
#   "#62BD80",
#   "#B2D135",
#   "#FCE533",
#   "#F39130",
#   "#ED4959"
# )

allshapes <- c(
  "none",
  "rectangle",
  "ellipse",
  "triangle",
  "rounded_rectangle",
  "text",
  "image"
)

colorchoice <- sample(allcolors, size = sample(c(1,2,3), size = 1))
shapechoice <- sample(c("ellipse",  "triangle", "rectangle", "rounded_rectangle"), size = sample(c(1,2,3), size = 1))

COLOR <- allcolors[allcolors %in% colorchoice]
NOCOLOR <- allcolors[!allcolors %in% colorchoice]

SHAPE <- allshapes[allshapes %in% shapechoice]
NOSHAPE <- allshapes[!allshapes %in% shapechoice]

shapeblocks <- function(data, name)
{
  div(style = paste0("
      margin: 5px;"
      # ",
      # if(name == "rectangle"){"border-radius: 2px;"}
      # else if(name == "rounded_rectangle"){"border-radius: 12px;"}
      # else if(name == "none"){""}
      # else if(name == "ellipse"){"border-radius: 50%;"}
      # else if(name == "triangle"){""}
      # else if(name == "text"){""}
      # else if(name == "image"){""},
      ),
      drag = name,
      id = name,
      class = "btn btn-default",
      class = "cloned",
      # if(name == "rectangle"){icon("square-full")}
      # else if(name == "rounded_rectangle"){icon("square")}
      # else if(name == "none"){icon("times-circle")}
      # else if(name == "ellipse"){icon("circle")}
      # else if(name == "triangle"){icon("caret-up")}
      # else if(name == "text"){icon("font")}
      # else if(name == "image"){icon("image")},
      name
  )
}

shapeblocks2 <- function(data, name)
{
  div(style = paste0("
      margin: 5px;"
      # ",
      #  if(name == "rectangle"){"border-radius: 2px;"}
      #  else if(name == "rounded_rectangle"){"border-radius: 12px;"}
      #  else if(name == "none"){""}
      #  else if(name == "ellipse"){"border-radius: 50%;"}
      #  else if(name == "triangle"){""}
      #  else if(name == "text"){""}
      #  else if(name == "image"){""},
                     ),
      drag = name,
      id = name,
      class = "btn btn-default",
      # if(name == "rectangle"){icon("square-full")}
      # else if(name == "rounded_rectangle"){icon("square")}
      # else if(name == "none"){icon("times-circle")}
      # else if(name == "ellipse"){icon("circle")}
      # else if(name == "triangle"){icon("caret-up")}
      # else if(name == "text"){icon("font")}
      # else if(name == "image"){icon("image")},
      name
  )
}

colorblocks <- function(data, name)
{
  div(style = paste0("
      border-color:", name, ";
      color: white;
      background-color:", name, ";
      margin: 5px;
      "),
      drag = name,
      id = name,
      class = "btn btn-default",
      class = "cloned2",
      name
  )
}

colorblocks2 <- function(data, name)
{
  div(style = paste0("
      border-color:", name, ";
      color: white;
      background-color:", name, ";
      margin: 5px;
      "),
      drag = name,
      id = name,
      class = "btn btn-default",
      name
  )
}