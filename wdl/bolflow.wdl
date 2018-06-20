# import "/mnt/projects/metabolomics/bolflow/wdl/setup.wdl" as setup

workflow bolFlow {
  String name
  Array[File] infiles
  File incfile
  # String inpath
  call joinFiles {
    input:
      sampleName=name,
      inFiles=infiles,
      classFile=incfile
  }
  call calcFreq {
    input:
      sampleName=name,
      inFile=joinFiles.outFile
  }
 call filtData {
    input:
      sampleName=name,
      inFile=calcFreq.outFile    
  }
  # call setup.copy {
  #   input:
  #     inFiles=[joinFiles.outFile, calcFreq.outFile,filtData.outFile]
  # }
}

# This task calls join_files script.
task joinFiles {
  String sampleName
  Array[File] inFiles
  File classFile
  command {
    python3 /home/docker/bolflow/join_files.py \
      -ii ${sep=" " inFiles} \
      -ic ${classFile} \
      -o ${sampleName}.join.csv
  }
  output {
    File outFile = "${sampleName}.join.csv"
  }
}

# This task calculates the frequency and standard desviation.
task calcFreq {
  String sampleName
  File inFile
  command {
    python3 /home/docker/bolflow/freq-cv.py \
      -i ${inFile} \
      -o ${sampleName}.freq-cv.csv
  }
  output {
    File outFile = "${sampleName}.freq-cv.csv"
  }
}

# This task filters by frequency and by cv. It also marks the duplicates.
task filtData {
  String sampleName
  File inFile
  Int filtFreq
  Int filtCV
  command {
    python3 /home/docker/bolflow/filter.py \
      -i ${inFile} \
      -ff ${filtFreq} \
      -fc ${filtCV} \
      -o ${sampleName}.freq-cv-filt.csv
  }
  output {
    File outFile = "${sampleName}.freq-cv-filt.csv"
  }
}
