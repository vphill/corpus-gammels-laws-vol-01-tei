<?xml version="1.0" encoding="utf-8"?>
 
<xsl:stylesheet xmlns:tei="http://www.tei-c.org/ns/1.0"
  xmlns="http://www.w3.org/1999/xhtml"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
 
  <xsl:output method="text" encoding="UTF-8" />
 
  <xsl:template match="tei:TEI">
    <xsl:apply-templates />
  </xsl:template>
 
<!-- Remove the punctuation when it is weak TODO make it only weak -->
<xsl:template match="pc">

</xsl:template>

  <xsl:template match="tei:teiHeader"></xsl:template>
 
</xsl:stylesheet>