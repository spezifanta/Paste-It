# -*- coding: utf-8 -*-

import random
import re
import string
from django.db import models

class Paste(models.Model):
    id = models.SlugField(max_length=6, primary_key=True)
    language = models.ForeignKey('Language')
    public = models.BooleanField('Public', default=0)
    title = models.CharField(max_length=32, blank=True)
    content = models.TextField('Content')
    #hl_lines = models.TextField()
    views = models.PositiveIntegerField(blank=True, default=0)
    last_paste = models.SlugField(max_length=6, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.language.name

    def get_title(self):
        title = ''
        limit = 64
        if len(self.content) <= limit:
            title = self.content
        else:
            lines = self.content.split('\n')
            for line in lines:
                if not line.strip():
                    continue
                if line.startswith('#'):
                    continue
                if len(title) > limit:
                    break
                title += line + '\n'

            title = title[:limit].rstrip()
            title = title.replace('\n', ' \\ ') + '...'

        return title

    def save(self, *args, **kwargs):
        # Update
        #if update:
        #    super(Paste, self).save(*args, **kwargs)

        # Generate a random Id
        self.id = ''.join([random.choice(string.letters + string.digits) for i in xrange(6)])

        # Clean up content
        self.content = self.content.replace('\r', '') # remove carriage return
        self.content = self.content.replace('\t', '    ') # replace tabs

        # Clean up whitespaces and empty lines
        lines = self.content.split('\n')
        new_content = []
        indentation_length = None
        for line in lines:
            # Skip empty lines at the beginning
            if not line.strip() and indentation_length is None:
                continue
            widthspace_match = re.match(r'^(?P<length>\s+).+', line)
            # Line starts with whitespaces
            if widthspace_match:
                length = len(widthspace_match.group('length'))
                if indentation_length is None or indentation_length > length:
                    indentation_length = length
                if indentation_length <= length:
                    new_content.append(line)
            # Line is empty
            elif not line.strip():
                new_content.append(line)
            # Line starts straight away
            else:
                indentation_length = 0
                new_content.append(line)

        # Strip unnecessary whitespace on the left and all on the right
        new_content = map(lambda line: line[indentation_length:].rstrip() + '\n', new_content)

        # Glue all back together and remove all whitespace at the end
        self.content = ''.join(new_content).rstrip()

        # Call the "real" save method
        super(Paste, self).save(*args, **kwargs)

    class Meta:
        db_table = 'pastes'
        get_latest_by = 'created'

class Language(models.Model):
    ext = models.SlugField(max_length=6, primary_key=True)
    name = models.CharField(max_length=32)
    short = models.CharField(max_length=32, blank=True)
    mimetype = models.CharField(max_length=64, blank=True)
    favorite = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'languages'
        ordering = ['name']
