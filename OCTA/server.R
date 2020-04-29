server = function(input, output, session) {
  
  # if (!Sys.info()[['sysname']] == 'Darwin'){
  #   # When running on shinyapps.io, create a virtualenv
  #   reticulate::virtualenv_create(envname = 'python35_env',
  #                                 python = '/usr/bin/python3')
  #   reticulate::virtualenv_install('python35_env',
  #                                  packages = c("svgwrite", "numpy", "colour", "pandas"))  # <- Add other packages here, if needed
  # }
  # reticulate::use_virtualenv('python35_env', required = T)
  # reticulate::source_python('OCTA_functions_inline_28_03_2020.py')
  
  parameters <- reactiveValues(nrows = NA, ncols = NA,
                               startx = NA, starty = NA, 
                               xdist = NA,  ydist = NA,
                               jitterscale = NA,
                               shape = NA,
                               shapepattern = NA, shapedim = NA,
                               shapesize = NA, shapexyratio = NA,
                               shapecolour = NA,
                               colourpattern = NA, colourdim = NA,
                               orientation = NA,
                               shapeorientationpattern = NA, shapeorientationdim = NA,
                               output = "txtinline"
  )
  
  observe({
    parameters$nrows  <- input$nrows
    parameters$ncols  <- input$ncols
    parameters$startx <- input$startx
    parameters$starty <- input$starty
    parameters$xdist  <- input$xdist
    parameters$ydist  <- input$ydist
    parameters$jitterscale  <- input$jitterscale
    parameters$shape        <- if(!is.null(input$shapedest_order$text)){input$shapedest_order$text}else{SHAPE}
    parameters$shapepattern <- input$shapepattern
    parameters$shapedim     <- input$shapedim
    parameters$shapesize    <- input$size
    parameters$shapexyratio <- input$shapexyratio
    parameters$shapepattern <- input$shapepattern
    parameters$shapedim     <- input$shapedim
    parameters$shapecolour  <- if(!is.null(input$colordest_order$text)){input$colordest_order$text}else{COLOR}
    parameters$colourpattern<- input$colorpattern
    parameters$colourdim    <- input$colordim   
    parameters$orientation  <- input$orientation
    parameters$shapeorientationpattern <- input$orientationpattern
    parameters$shapeorientationdim     <- input$orientationdim
  })
  
  table <- reactiveValues(display = NA, elements = NA) 
  
  observe({
    table$display <- data.frame(nrows = parameters$nrows, ncols = parameters$ncols,
                                startx = parameters$startx, starty = parameters$starty,
                                xdist = parameters$xdist, ydist = parameters$ydist,
                                jitterscale = parameters$jitterscale,
                                shape = I(list(parameters$shape)),
                                shapepattern = parameters$shapepattern,
                                shapedim = parameters$shapedim,
                                # text = "OCTA",
                                # image = "../vector_images/OCTA_animatedflower.svg",
                                shapesize = I(list(parameters$shapesize)),
                                shapexyratio = I(list(parameters$shapexyratio)),
                                shapecolour = I(list(parameters$shapecolour)),
                                colourpattern = parameters$colourpattern,
                                colourdim = parameters$colourdim,
                                orientation = I(list(parameters$orientation)),
                                shapeorientationpattern = parameters$shapeorientationpattern,
                                shapeorientationdim = parameters$shapeorientationdim,
                                output = "txtinline")
    
    table$elements <- create_pattern_json(
                                nrows = parameters$nrows, ncols = parameters$ncols,
                                startx = parameters$startx, starty = parameters$starty,
                                xdist = parameters$xdist, ydist = parameters$ydist,
                                jitterscale = parameters$jitterscale,
                                shape = parameters$shape,
                                shapepattern = parameters$shapepattern,
                                shapedim = parameters$shapedim,
                                # text = "OCTA",
                                # image = "../vector_images/OCTA_animatedflower.svg",
                                shapesize = as.numeric(parameters$shapesize),
                                shapexyratio = as.numeric(parameters$shapexyratio),
                                shapecolour = parameters$shapecolour,
                                colourpattern = parameters$colourpattern,
                                colourdim = parameters$colourdim,
                                orientation = as.numeric(parameters$orientation),
                                shapeorientationpattern = parameters$shapeorientationpattern,
                                shapeorientationdim = parameters$shapeorientationdim,
                                output = "txtinline")
  })
  
  # observeEvent(input$parametershot, {
  #   table$display <- hot_to_r(input$parametershot)
  #   table$elements <- create_pattern_json(
  #                         nrows = parameters$nrows, ncols = parameters$ncols,
  #                         startx = parameters$startx, starty = parameters$starty,
  #                         xdist = parameters$xdist, ydist = parameters$ydist,
  #                         jitterscale = parameters$jitterscale,
  #                         shape = I(list(parameters$shape)),
  #                         shapepattern = parameters$shapepattern,
  #                         shapedim = parameters$shapedim,
  #                         # text = "OCTA",
  #                         # image = "../vector_images/OCTA_animatedflower.svg",
  #                         #shapesize = I(list(parameters$shapesize)),
  #                         shapexyratio = as.numeric(parameters$shapexyratio),
  #                         shapecolour = I(list(parameters$shapecolour)),
  #                         colourpattern = parameters$colourpattern,
  #                         colourdim = parameters$colourdim,
  #                         orientation = parameters$orientation,
  #                         shapeorientationpattern = parameters$shapeorientationpattern,
  #                         shapeorientationdim = parameters$shapeorientationdim,
  #                         output = "txtinline")
  # })
  
  observeEvent(input$hot, {
    table$elements <- hot_to_r(input$hot)
  })
  
  svg <- reactive({
    create_pattern_fromtxt_inline(table$elements, output = "svginline")
  })
  
  output$svgplot = renderUI({
    
    # Return a list containing the filename
    HTML(noquote(paste0("<center>", svg(), "</center>")))
  })
  
  output$svgplot2 = renderUI({
    
    # Return a list containing the filename
    HTML(noquote(paste0("<center>", svg(), "</center>")))
  })
  
  output$svgplot3 = renderUI({
    
    # Return a list containing the filename
    HTML(noquote(paste0("<center>", svg(), "</center>")))
  })
  
  output$svgplot4 = renderUI({
    
    # Return a list containing the filename
    HTML(noquote(paste0("<center>", svg(), "</center>")))
  })
  
  output$svgplot5 = renderUI({
    
    # Return a list containing the filename
    HTML(noquote(paste0("<center>", svg(), "</center>")))
  })
  
  output$svgplot6 = renderUI({
    
    # Return a list containing the filename
    HTML(noquote(paste0("<center>", svg(), "</center>")))
  })
  
  output$svgplot7 = renderUI({
    
    # Return a list containing the filename
    HTML(noquote(paste0("<center>", svg(), "</center>")))
  })
  
  output$svgprint = renderPrint({
    
    # Return a list containing the filename
    cat(noquote(paste0(svg())))
  })
  
  output$downloadsvg <- downloadHandler(
    filename = function() {
      paste0("OCTA_", format(Sys.time(), format = "%Y-%j-%H%M%S"), ".svg")
    },
    content = function(file) {
      write.table(x = noquote(svg()), file, row.names = FALSE, quote = F, col.names = F)
    }
  )
  
  output$downloadjson <- downloadHandler(
    filename = function() {
      paste0("OCTA_", format(Sys.time(), format = "%Y-%j-%H%M%S"), ".json")
    },
    content = function(file) {
      write_json(x = noquote(toJSON(list(display = table$display, elements = table$elements), pretty = T)), path = file)
    }
  )
  
  output$downloadtxt <- downloadHandler(
    filename = function() {
      paste0("OCTA_elements_", format(Sys.time(), format = "%Y-%j-%H%M%S"), ".txt")
    },
    content = function(file) {
      write.table(x = noquote(table$elements), file, row.names = FALSE, quote = F, col.names = T)
    }
  )
  
  output$downloadtxtparams <- downloadHandler(
    filename = function() {
      paste0("OCTA_params_", format(Sys.time(), format = "%Y-%j-%H%M%S"), ".txt")
    },
    content = function(file) {
      write.table(x = noquote(table$display), file, row.names = FALSE, quote = F, col.names = T)
    }
  )
  
  output$hot = renderRHandsontable({
    
    rhandsontable(table$elements %>% select(x, y, shape, xyratio, colour, size, shapeorientation, mirror, everything())) %>%
      hot_table(highlightCol = TRUE, highlightRow = TRUE) %>%
      hot_col(c("max_x", "max_y", "xdist", "ydist",
                "shaperepeat", "colourpattern", "colourdim", "colourrepeat", 
                "number", "column", 
                "xjitter", "yjitter"), readOnly = TRUE)
  })   
  
  output$parametershot = renderRHandsontable({
    
    rhandsontable(table$display) %>%
      hot_table(highlightCol = TRUE, highlightRow = TRUE) 
  }) 
  
}