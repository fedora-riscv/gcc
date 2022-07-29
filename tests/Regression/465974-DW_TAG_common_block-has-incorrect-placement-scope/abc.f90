      subroutine a
      INTEGER*4 a_i
      common /block/a_i
      a_i = 1
      end subroutine a
      subroutine b
      INTEGER*4 b_i
      common /block/b_i
      a_i = 3
      b_i = 2
      end subroutine b
      subroutine c
      INTEGER*4 a_i
      common /block/a_i
      if (a_i .ne. 2) call abort
      end subroutine c
      program abc
      call a
      call b
      call c
      end program abc

