#/!bin/bash
# Bundles code for submission
TAR_PATH=billg.tar.gz
rm -rf ${TAR_PATH}
COPYFILE_DISABLE=1 tar czvf $TAR_PATH {src,test,lib}/ test.sh